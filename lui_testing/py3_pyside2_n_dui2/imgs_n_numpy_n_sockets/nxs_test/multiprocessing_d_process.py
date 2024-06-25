from multiprocessing import Process
import os

def f(name):
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print('hello', name)

if __name__ == '__main__':

    for repetn in range(5):
        name = "clone # " + str(repetn)
        p = Process(target=f, args=(name,))
        p.start()
        p.join()
