import os, shutil

    to_test = '''
    my_tst_path = os.environ["PWD"]
    print("my_tst_path =", my_tst_path, "\n")
    print("os.get_exec_path =", os.get_exec_path())
    print("os.pathsep =", os.pathsep)
    print("os.path.abspath =", os.path.abspath("."))
    print("os.getcwd =", os.getcwd())
    print("os.sep =", os.sep)
    '''


def create_dir():
    path2add = os.getcwd() + os.sep + "here"
    try:
        shutil.rmtree(path2add)

    except FileNotFoundError:
        print("No need to remove non existent dir")

    os.mkdir(path2add)
    return path2add

if __name__ == "__main__":

    new_dir = create_dir()
    print("new_dir =", new_dir)
