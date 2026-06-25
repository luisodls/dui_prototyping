#from PySide6.QtCore import QThread, QMutex, QWaitCondition
from PySide2.QtCore import QThread, QMutex, QWaitCondition

from threading import Event

class WorkTH(QThread):
    def __init__(self):
        super().__init__()
        self.result = None
        self._done = Event()

    def run(self):
        import time
        time.sleep(2)
        self.result = "hello from thread(run)"
        self._done.set()       # like wakeAll()

    def get_result(self):
        self._done.wait()      # like your while loop, but no CPU burning
        return self.result


w_t1 = WorkTH()
w_t1.start()

print("waiting for result...")
print(w_t1.get_result())   # blocks here until run() calls wakeAll()
print("done")
