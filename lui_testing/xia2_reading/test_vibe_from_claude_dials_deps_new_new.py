import sys, json, os, io, contextlib, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vibe_from_claude_dials_deps_new_new as m

def check(name, got, exp):
    print(("PASS " if got == exp else "FAIL ") + name + ("" if got == exp else "  got=%r exp=%r" % (got, exp)))

# split_cmd_line
check("split no args", m.split_cmd_line("xia2.report"), ("xia2.report", []))
check("split normal", m.split_cmd_line("dials.index  'a.expt' 'b.refl' 'x=1'"), ("dials.index", ["a.expt", "b.refl", "x=1"]))
check("split one arg", m.split_cmd_line("prog 'a.expt'"), ("prog", ["a.expt"]))
check("split duplicate args kept", m.split_cmd_line("prog 'a' 'a'"), ("prog", ["a", "a"]))
# reversed_find_str
check("rfs path", m.reversed_find_str("/a/b/c.expt"), "c.expt")
check("rfs trailing sep", m.reversed_find_str("a/b/"), "")
check("rfs none", m.reversed_find_str("c.expt"), "c.expt")
# is_output_key
for k, e in [("output.experiments", True), ("mtz.hklout", True), ("hklout", True), ("json", True),
             ("debug.reference.output", True), ("outlier.algorithm", False), ("input.experiments", False),
             ("output_prefix", False)]:
    check("is_output_key " + k, m.is_output_key(k), e)
# classify
check("classify mixed", m.classify_params([
    "input.experiments=/p/a.expt", "b.refl", "output.experiments=c.expt", "output.project_name=AUTO",
    "debug.reference.output=True", "dispersion.kernel_size=3 3", "hklin", "d.mtz", "hklout", "e.mtz", "nproc=4"]),
    (["a.expt", "b.refl", "d.mtz", "4"], ["c.expt", "e.mtz"]))
check("classify hklin at end (no value)", m.classify_params(["hklin"]), (["hklin"], []))
check("bravais", [m.is_bravais_setting(x) for x in ["bravais_setting_9.expt", "bravais_setting_.expt", "bravais_setting_x.expt"]], [True, False, False])

def run(entries):
    fd, p = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(entries, f)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return m.get_list_of_commands(p)
    finally:
        os.remove(p)

# multi-sweep: two parents with same type of file, plus file rewritten later
cmds = run([
    {"command": "dials.integrate 'a.expt' 'output.experiments=s1.expt' 'output.reflections=s1.refl'"},
    {"command": "dials.integrate 'b.expt' 'output.experiments=s2.expt' 'output.reflections=s2.refl'"},
    {"command": "dials.scale 's1.expt' 's1.refl' 's2.expt' 's2.refl' 'output.experiments=sc.expt'"},
    {"command": "dials.integrate 'c.expt' 'output.experiments=s1.expt'"},
    {"command": "dials.symmetry 's1.expt'"},
])
check("multi-parent", cmds[2]['parent_pos_lst'], [0, 1])
check("children", (cmds[0]['chidren_pos_lst'], cmds[1]['chidren_pos_lst']), ([2], [2]))
check("rewritten file -> latest writer", cmds[4]['parent_pos_lst'], [3])
check("externals", cmds[0]['external_files_lst'], ["a.expt"])
check("no times ok", cmds[0]['time_start'], None)
with contextlib.redirect_stdout(io.StringIO()):
    m.print_commands(cmds)   # must not crash without timing
    m.print_commands([])
print("PASS print without timing / empty")

# param links: no refine_bravais/symmetry earlier -> no link, no crash
cmds = run([{"command": "dials.reindex 'x.refl' 'change_of_basis_op=a,b,c'"},
            {"command": "convert-mtz-sca"}])
check("param link without producer", cmds[0]['parent_pos_lst'], [])
check("implicit prev", cmds[1]['parent_pos_lst'], [0])
cmds = run([{"command": "convert-mtz-sca"}])
check("implicit at position 0", cmds[0]['parent_pos_lst'], [])
check("empty file", run([]), [])
