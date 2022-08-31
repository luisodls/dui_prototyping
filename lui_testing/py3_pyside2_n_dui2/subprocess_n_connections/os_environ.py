import subprocess
import os

def run_cmd(cmd_to_run):
    proc = subprocess.Popen(
        cmd_to_run,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    line = None
    while proc.poll() is None or line != '':
        line = proc.stdout.readline()[:-1]
        print("line>>", line)

    proc.stdout.close()


if __name__ == "__main__":
    cmd_lst = [
        "dials.find_spots",
        "dials.index",
        "dials.refine",
        "dials.integrate",
        "dials.scale",
        ]

    for comd in cmd_lst:
        run_cmd(str(comd))



