import subprocess
import os

def run_cmd_tst(cmd_lst_2_run):
    try:
        proc = subprocess.run(
            cmd_lst_2_run, shell = False, capture_output = True, timeout = 5
        )
        if proc.returncode == 0:
            success = True

        else:
            success = False
            print("return code =", proc.returncode)

    except FileNotFoundError:
        success = False
        print("FileNotFoundError")

    except PermissionError:
        success = False
        print("PermissionError")

    return success


if __name__ == "__main__":
    #cmd_lst = ["ls", "-al"]
    #cmd_lst = ["./a.out"]
    #cmd_lst = ["dials.import", "-h"]
    cmd_lst = ["cloudrun", "aaaa"]

    cmd_success = run_cmd_tst(cmd_lst)
    print("cmd_success =", cmd_success)



