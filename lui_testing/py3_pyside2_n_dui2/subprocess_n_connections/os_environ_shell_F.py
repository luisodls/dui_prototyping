import subprocess
import os

def run_cmd(cmd_to_run):


    my_env = os.environ.copy()
    print("my_env =", my_env)
    my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
    '''
    subprocess.Popen(my_command, env=my_env)
    '''

    proc = subprocess.Popen(
        cmd_to_run,
        shell=False,
        env=my_env,
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
        run_cmd([str(comd)+".exe", "-c"])



