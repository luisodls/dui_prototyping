import os

if __name__ == "__main__":
    my_tst_path = os.environ["PWD"]
    print("my_tst_path =", my_tst_path, "\n")
    print("os.get_exec_path =", os.get_exec_path())
    print("os.pathsep =", os.pathsep)
    print("os.path.abspath =", os.path.abspath("."))
    print("os.getcwd =", os.getcwd())
    print("os.sep =", os.sep)
