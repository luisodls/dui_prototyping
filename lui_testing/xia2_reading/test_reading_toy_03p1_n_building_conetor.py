import sys, os, io, contextlib, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reading_toy_03p1_n_building_conetor as m

n_fail = 0

def check(name, got, exp):
    global n_fail
    if got != exp:
        n_fail += 1
    print(("PASS " if got == exp else "FAIL ") + name + ("" if got == exp else "  got=%r exp=%r" % (got, exp)))

# split_cmd_line
check("split no args", m.split_cmd_line("xia2.report\n"), ("xia2.report", ["xia2.report"]))
check("split normal", m.split_cmd_line(" dials.index  'a.expt' 'b.refl' 'x=1'\n"),
      ("dials.index", ["dials.index", "a.expt", "b.refl", "x=1"]))
check("split one arg", m.split_cmd_line("prog 'a.expt'"), ("prog", ["prog", "a.expt"]))
check("split duplicate args removed", m.split_cmd_line("prog 'a' 'b' 'a'"), ("prog", ["prog", "a", "b"]))
check("split empty arg dropped", m.split_cmd_line("prog '' 'a'"), ("prog", ["prog", "a"]))
check("split arg with space", m.split_cmd_line("prog 'k=3 3'"), ("prog", ["prog", "k=3 3"]))

# classify_params (first item is the program name, it is not classified)
check("classify dials.find_spots", m.classify_params([
    "dials.find_spots", "input.experiments=1_SWEEP1_masked.expt",
    "output.experiments=2_SWEEP1_strong.expt", "output.reflections=2_SWEEP1_strong.refl",
    "nproc=24", "dispersion.kernel_size=3 3", "write_hot_mask=true"]),
    (["input.experiments=1_SWEEP1_masked.expt"],
     ["output.experiments=2_SWEEP1_strong.expt", "output.reflections=2_SWEEP1_strong.refl"],
     ["nproc=24", "dispersion.kernel_size=3 3", "write_hot_mask=true"]))
check("classify bare files and phil", m.classify_params(
    ["prog", "/p/a.expt", "b.refl", "1_mask.phil", "something"]),
    (["/p/a.expt", "b.refl", "1_mask.phil"], [], ["something"]))
check("classify output without file", m.classify_params(
    ["prog", "output.project_name=AUTOMATIC", "debug.reference.output=True", "json=3_blanks.json"]),
    ([], ["json=3_blanks.json"], ["output.project_name=AUTOMATIC", "debug.reference.output=True"]))
check("classify input key without extension", m.classify_params(
    ["prog", "input.experiments=/p/no_ext"]), (["input.experiments=/p/no_ext"], [], []))
check("classify key=file is input", m.classify_params(
    ["prog", "reflections=/p/18_scaled.refl", "mtz.hklout=x.mtz"]),
    (["reflections=/p/18_scaled.refl"], ["mtz.hklout=x.mtz"], []))
check("classify positional pairs", m.classify_params(
    ["freerflag", "hklin", "/p/a.mtz", "hklout", "b.mtz", "xyzin", "c.pdb"]),
    (["/p/a.mtz", "c.pdb"], ["b.mtz"], []))
check("classify hklin at end (no value)", m.classify_params(["prog", "hklin"]), ([], [], ["hklin"]))
check("classify param values", m.classify_params(
    ["prog", "change_of_basis_op=b,c,a", "space_group=75", "cut_data.d_min=1.1"]),
    ([], [], ["change_of_basis_op=b,c,a", "space_group=75", "cut_data.d_min=1.1"]))
check("classify nothing", m.classify_params(["xia2.report"]), ([], [], []))

# split_by_type (paths and "key=" are removed)
check("split_by_type", m.split_by_type(
    ["input.experiments=/p/a.expt", "b.refl", "/p/c.mtz", "d.expt", "x.refl.bz2"]),
    (["a.expt", "d.expt"], ["b.refl"], ["c.mtz", "x.refl.bz2"]))
check("split_by_type empty", m.split_by_type([]), ([], [], []))

# add_connection
def blank(pos):
    return {'curr_poss': pos, 'parent_pos_lst': [], 'chidren_pos_lst': [],
            'files_from_parent_dict': {}}

p0, p1, c = blank(0), blank(1), blank(2)
m.add_connection(p0, c, "a.expt")
m.add_connection(p0, c, "a.refl")
m.add_connection(p1, c, "space_group=89")
check("add_connection parents", c['parent_pos_lst'], [0, 1])
check("add_connection children once", (p0['chidren_pos_lst'], p1['chidren_pos_lst']), ([2], [2]))
check("add_connection labels", c['files_from_parent_dict'], {0: ["a.expt", "a.refl"], 1: ["space_group=89"]})

# get_list_of_commands, on a small file in the xia2-debug.txt format
def run(cmd_lines):
    txt = "some log line\n"
    for cmd_str in cmd_lines:
        txt += "# command line:\n# " + cmd_str + "\n#\n# timing information:\nmore log\n"

    fd, p = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write(txt)

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return m.get_list_of_commands(p)

    finally:
        os.remove(p)

cmds = run([
    "dials.integrate  'input.experiments=/p/a.expt' 'output.experiments=s1.expt' 'output.reflections=s1.refl'",
    "dials.report  's1.expt' 's1.refl' 'output.html=r.html'",
    "dials.integrate  'b.expt' 'output.experiments=s2.expt' 'output.reflections=s2.refl'",
    "dials.scale  's1.expt' 's1.refl' 's2.expt' 's2.refl' 'output.experiments=sc.expt'",
    "dials.integrate  'c.expt' 'output.experiments=s1.expt'",
    "dials.symmetry  '/far/away/s1.expt'",
])
check("dials.report skipped", [d['exe_cmd'] for d in cmds],
      ["dials.integrate", "dials.integrate", "dials.scale", "dials.integrate", "dials.symmetry"])
check("positions renumbered", [d['curr_poss'] for d in cmds], [0, 1, 2, 3, 4])
check("multi-parent", cmds[2]['parent_pos_lst'], [0, 1])
check("multi-parent labels", cmds[2]['files_from_parent_dict'], {0: ["s1.expt", "s1.refl"], 1: ["s2.expt", "s2.refl"]})
check("children", (cmds[0]['chidren_pos_lst'], cmds[1]['chidren_pos_lst']), ([2], [2]))
check("rewritten file -> latest writer, path ignored", cmds[4]['parent_pos_lst'], [3])
check("externals", (cmds[0]['external_files_lst'], cmds[1]['external_files_lst']), (["a.expt"], ["b.expt"]))
check("tuning kept", cmds[0]['tuning_params_lst'], [])

cmds = run([
    "dials.index  'imported.expt' 'strong.refl' 'output.experiments=5_indexed.expt' 'output.reflections=5_indexed.refl'",
    "dials.refine_bravais_settings  '5_indexed.expt' '5_indexed.refl'",
    "dials.reindex  '5_indexed.refl' 'change_of_basis_op=b,c,a' 'space_group=75' 'output.reflections=8_reindexed.refl'",
    "dials.refine  'bravais_setting_9.expt' '8_reindexed.refl' 'output.experiments=9_refined.expt'",
    "dials.estimate_resolution  '9_refined.expt'",
    "dials.scale  '9_refined.expt' 'cut_data.d_min=1.1' 'nproc=4'",
])
check("param link from bravais", cmds[2]['files_from_parent_dict'],
      {0: ["5_indexed.refl"], 1: ["change_of_basis_op=b,c,a", "space_group=75"]})
check("implicit bravais_setting file", cmds[3]['files_from_parent_dict'],
      {1: ["bravais_setting_9.expt"], 2: ["8_reindexed.refl"]})
check("param link d_min", cmds[5]['files_from_parent_dict'],
      {3: ["9_refined.expt"], 4: ["cut_data.d_min=1.1"]})
check("nproc is not a link", cmds[5]['parent_pos_lst'], [3, 4])

cmds = run(["dials.reindex  'x.refl' 'change_of_basis_op=a,b,c'"])
check("param link without producer", cmds[0]['parent_pos_lst'], [])
cmds = run(["dials.refine  'bravais_setting_9.expt'"])
check("bravais file without producer is external", cmds[0]['external_files_lst'], ["bravais_setting_9.expt"])
check("empty file", run([]), [])

# whole xia2 run in tst5, if it is there
debug_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tst5", "xia2-debug.txt"
)
if os.path.exists(debug_path):
    with contextlib.redirect_stdout(io.StringIO()):
        cmds = m.get_list_of_commands(debug_path)

    edge_lst = []
    for d in cmds:
        for parent_poss in d['parent_pos_lst']:
            edge_lst.append((parent_poss, d['curr_poss']))

    check("tst5 number of commands", len(cmds), 23)
    check("tst5 number of connections", len(edge_lst), 31)
    check("tst5 no dials.report", "dials.report" in [d['exe_cmd'] for d in cmds], False)
    check("tst5 bravais -> reindex", cmds[6]['files_from_parent_dict'][5], ["change_of_basis_op=b,c,a", "space_group=75"])
    check("tst5 bravais -> refine", cmds[7]['files_from_parent_dict'][5], ["bravais_setting_9.expt"])
    check("tst5 estimate_resolution -> scale", cmds[14]['files_from_parent_dict'][13], ["cut_data.d_min=1.1"])
    check("tst5 merge -> FrenchWilson", (cmds[20]['exe_cmd'], cmds[20]['parent_pos_lst']), ("cctbx_FrenchWilson", [18]))

else:
    print("SKIP tst5 checks, not found:", debug_path)

print("\n%d failed" % n_fail)
sys.exit(1 if n_fail else 0)
