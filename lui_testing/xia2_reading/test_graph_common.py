import sys, os, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graph_common as g

n_fail = 0

def check(name, got, exp):
    global n_fail
    if got != exp:
        n_fail += 1
    print(("PASS " if got == exp else "FAIL ") + name + ("" if got == exp else "  got=%r exp=%r" % (got, exp)))

def cmd(pos, exe, parents = None):
    # minimal command dict, only the keys graph_common reads
    parents = parents or {}
    return {'curr_poss': pos, 'exe_cmd': exe,
            'parent_pos_lst': list(parents), 'files_from_parent_dict': parents}

# reversed_find_str
check("rfs path", g.reversed_find_str("/a/b/c.expt"), "c.expt")
check("rfs key=value", g.reversed_find_str("nproc=4"), "4")
check("rfs key=path", g.reversed_find_str("input.experiments=/p/a.expt"), "a.expt")
check("rfs none", g.reversed_find_str("c.expt"), "c.expt")
check("rfs trailing sep", g.reversed_find_str("a/b/"), "")
check("rfs only path sep keeps =", g.reversed_find_str("x=/p/a=b.expt", lst_sep_lst = [os.sep]), "a=b.expt")
check("rfs only path sep no path", g.reversed_find_str("x=1", lst_sep_lst = [os.sep]), "x=1")

# is_output_key
for k, e in [("output.experiments", True), ("output.html", True), ("mtz.hklout", True),
             ("mmcif.hklout", True), ("hklout", True), ("json", True),
             ("debug.reference.output", True), ("outlier.algorithm", False),
             ("input.experiments", False), ("output_prefix", False), ("", False)]:
    check("is_output_key " + repr(k), g.is_output_key(k), e)

# has_file_extension
for f, e in [("a.expt", True), ("a.refl", True), ("x.mmcif.bz2", True), ("a.mtz", True),
             ("a.txt", False), ("expt", False), ("", False), ("a.expt.tmp", False)]:
    check("has_file_extension " + repr(f), g.has_file_extension(f), e)

# is_bravais_setting / is_bravais_summary
for f, e in [("bravais_setting_9.expt", True), ("bravais_setting_12.expt", True),
             ("bravais_setting_.expt", False), ("bravais_setting_x.expt", False),
             ("bravais_setting_9.refl", False), ("my_bravais_setting_9.expt", False)]:
    check("is_bravais_setting " + f, g.is_bravais_setting(f), e)

check("is_bravais_summary yes", g.is_bravais_summary("bravais_summary.json"), True)
check("is_bravais_summary no", g.is_bravais_summary("5_bravais_summary.json"), False)

# find_implicit_parent: most recent run of the writing program
prev = [cmd(0, "dials.index"), cmd(1, "dials.refine_bravais_settings"),
        cmd(2, "dials.reindex"), cmd(3, "dials.refine_bravais_settings"), cmd(4, "dials.refine")]
check("implicit setting -> latest bravais", g.find_implicit_parent("bravais_setting_9.expt", prev), 3)
check("implicit summary -> latest bravais", g.find_implicit_parent("bravais_summary.json", prev), 3)
check("implicit only first run", g.find_implicit_parent("bravais_setting_9.expt", prev[0:3]), 1)
check("implicit no writer yet", g.find_implicit_parent("bravais_setting_9.expt", prev[0:1]), None)
check("implicit normal file", g.find_implicit_parent("5_indexed.expt", prev), None)
check("implicit empty prev", g.find_implicit_parent("bravais_setting_9.expt", []), None)

# find_param_parent: most recent run of any of the listed programs
prev = [cmd(0, "dials.refine_bravais_settings"), cmd(1, "dials.reindex"),
        cmd(2, "dials.symmetry"), cmd(3, "dials.estimate_resolution"), cmd(4, "dials.scale")]
check("param cob -> latest symmetry", g.find_param_parent("change_of_basis_op=a,b,c", prev), 2)
check("param cob -> bravais", g.find_param_parent("change_of_basis_op=a,b,c", prev[0:2]), 0)
check("param space_group", g.find_param_parent("space_group=89", prev), 2)
check("param d_min", g.find_param_parent("cut_data.d_min=1.1", prev), 3)
check("param d_min no producer", g.find_param_parent("cut_data.d_min=1.1", prev[0:3]), None)
check("param other key", g.find_param_parent("nproc=4", prev), None)
check("param key prefix only", g.find_param_parent("space_group_x=4", prev), None)
check("param bare d_min", g.find_param_parent("d_min=1.1", prev), None)
check("param empty prev", g.find_param_parent("space_group=89", []), None)

# short_label
check("short param kept", g.short_label("change_of_basis_op=-x,y,-z"), "change_of_basis_op=-x,y,-z")
check("short d_min kept", g.short_label("cut_data.d_min=1.1"), "cut_data.d_min=1.1")
check("short key=path", g.short_label("input.experiments=/p/q/10_refined.expt"), "10_refined.expt")
check("short path", g.short_label("/p/q/a.mtz"), "a.mtz")
check("short plain", g.short_label("12_integrated.refl"), "12_integrated.refl")
check("short implicit", g.short_label("(implicit)"), "(implicit)")

# print_graph_table
def table_rows(list_of_commands):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        g.print_graph_table(list_of_commands)
    lines = out.getvalue().split("\n")
    start = lines.index("-" * 90) + 1
    end = lines.index("=" * 90, start)
    return [l.split() for l in lines[start:end]], lines[start - 2]

cmds = [
    cmd(0, "dials.scale"),
    cmd(1, "dials.two_theta_refine"),
    cmd(2, "dials.merge", {1: ["/p/20_refined_cell.expt"], 0: ["reflections=/p/18_scaled.refl"]}),
    cmd(3, "dials.reindex", {2: ["space_group=89", "change_of_basis_op=b,c,a"]}),
]
rows, header = table_rows(cmds)
check("table header", header.split(), ["from", "parent", "to", "child", "via"])
check("table rows, parents sorted", rows, [
    ["0", "dials.scale", "2", "dials.merge", "18_scaled.refl"],
    ["1", "dials.two_theta_refine", "2", "dials.merge", "20_refined_cell.expt"],
    ["2", "dials.merge", "3", "dials.reindex", "change_of_basis_op=b,c,a,", "space_group=89"],
])
rows, header = table_rows([])
check("table empty", rows, [])
rows, header = table_rows([cmd(0, "xia2.report")])
check("table no connections", rows, [])

print("\n%d failed" % n_fail)
sys.exit(1 if n_fail else 0)
