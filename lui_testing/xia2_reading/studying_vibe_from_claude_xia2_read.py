#!/usr/bin/env python
"""
Reconstruct which command depends on which from an xia2 timing_data.json.

Each entry's command line is parsed; arguments that name output files
(output.*, *hklout, json=, ...) are recorded as produced by that command.
Any argument of a later command whose basename matches a produced file is
treated as an input coming from that producer.

Usage:

    cd /path/to/where/I/want/to/run/xia2

    source '/path/to/ccp4-9/bin/ccp4.setup-sh'
    source /path/to/Dials-3.30.1/dials

    xia2 --integrate --timing ~/path/to/images/dir/

    #optional
    find . -type f -name "*.json"

    dials.python /path/to/this/file...py [xia2-timing.json] [--dot deps.dot]
"""

import argparse
import json
import os
import re
import shlex

# Parameter names (the part before "=") that denote files written by the command
OUTPUT_KEY = re.compile(r"(^|\.)(output|hklout|json)(\.|$)|hklout$|^output\.")

# Positional keyword pairs used by CCP4-style programs, e.g. freerflag
POSITIONAL_IN = {"hklin", "xyzin"}
POSITIONAL_OUT = {"hklout", "xyzout"}

# Files written under default names that never appear as output arguments.
# Maps a regex on the input basename to the program that implicitly wrote it.
IMPLICIT_OUTPUTS = [
    (re.compile(r"^bravais_setting_\d+\.expt$"), "dials.refine_bravais_settings"),
    (re.compile(r"^bravais_summary\.json$"), "dials.refine_bravais_settings"),
]

FILE_EXT = re.compile(
    r"\.(expt|refl|mtz|mmcif|cif|json|phil|mask|sca|p4p|html|log|bz2)$"
)


def parse_command(cmd):
    """Return (program, inputs, outputs) with basenames of the files."""
    tokens = shlex.split(cmd)
    program, args = tokens[0], tokens[1:]
    inputs, outputs = [], []
    i = 0
    while i < len(args):
        tok = args[i]
        if tok in POSITIONAL_IN | POSITIONAL_OUT and i + 1 < len(args):
            target = outputs if tok in POSITIONAL_OUT else inputs
            target.append(os.path.basename(args[i + 1]))
            i += 2
            continue
        if "=" in tok:
            key, value = tok.split("=", 1)
            # skip parameter values that clearly are not file names
            if " " in value or not value:
                i += 1
                continue
            if OUTPUT_KEY.search(key):
                # ignore non-file outputs such as output.project_name=AUTOMATIC
                if "." in os.path.basename(value):
                    outputs.append(os.path.basename(value))
            else:
                inputs.append(os.path.basename(value))
        else:
            inputs.append(os.path.basename(tok))
        i += 1
    return program, inputs, outputs


def build_graph(entries):
    steps = []
    producer_of = {}  # basename -> index of the most recent step that wrote it
    for idx, entry in enumerate(entries):
        program, inputs, outputs = parse_command(entry["command"])
        deps = []  # (producer index or None, file basename)
        for name in inputs:
            if name in producer_of:
                deps.append((producer_of[name], name))
                continue
            implicit = None
            for pattern, prog in IMPLICIT_OUTPUTS:
                if pattern.match(name):
                    # most recent earlier run of that program
                    for j in range(idx - 1, -1, -1):
                        if steps[j]["program"] == prog:
                            implicit = j
                            break
            if implicit is not None:
                deps.append((implicit, name))
            elif FILE_EXT.search(name):
                deps.append((None, name))  # external / unknown origin
        steps.append(
            {
                "index": idx,
                "program": program,
                "outputs": outputs,
                "deps": deps,
                "start": entry.get("time_start"),
                "end": entry.get("time_end"),
            }
        )
        for name in outputs:
            producer_of[name] = idx
    return steps


def print_report(steps):
    t0 = steps[0]["start"] if steps and steps[0]["start"] else 0.0
    for s in steps:
        timing = ""
        if s["start"] is not None and s["end"] is not None:
            timing = "  (t=%.1fs, %.1fs)" % (s["start"] - t0, s["end"] - s["start"])
        print("[%d] %s%s" % (s["index"], s["program"], timing))
        by_producer = {}
        for producer, name in s["deps"]:
            by_producer.setdefault(producer, []).append(name)
        for producer in sorted(by_producer, key=lambda p: (p is None, p)):
            names = ", ".join(sorted(set(by_producer[producer])))
            if producer is None:
                print("      <- external: %s" % names)
            else:
                print(
                    "      <- [%d] %s: %s"
                    % (producer, steps[producer]["program"], names)
                )
        if s["outputs"]:
            print("      -> %s" % ", ".join(s["outputs"]))


def write_dot(steps, path):
    with open(path, "w") as f:
        f.write("digraph deps {\n  rankdir=TB;\n  node [shape=box];\n")
        for s in steps:
            f.write('  n%d [label="[%d] %s"];\n' % (s["index"], s["index"], s["program"]))
        edges = {}
        for s in steps:
            for producer, name in s["deps"]:
                if producer is not None:
                    edges.setdefault((producer, s["index"]), set()).add(name)
        for (a, b), names in sorted(edges.items()):
            label = "\\n".join(sorted(names))
            f.write('  n%d -> n%d [label="%s", fontsize=9];\n' % (a, b, label))
        f.write("}\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("timing_file", nargs="?", default="timing_data.json")
    parser.add_argument("--dot", help="also write a Graphviz .dot file")
    args = parser.parse_args()

    with open(args.timing_file) as f:
        entries = json.load(f)
    steps = build_graph(entries)
    print_report(steps)
    if args.dot:
        write_dot(steps, args.dot)
        print("\nGraphviz file written to %s (render: dot -Tpng %s -o deps.png)"
              % (args.dot, args.dot))


if __name__ == "__main__":
    main()
