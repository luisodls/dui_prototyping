#from PySide6.QtCore import QThread, QMutex, QWaitCondition
from PySide2.QtCore import QThread, QMutex, QWaitCondition

class WorkTH(QThread):
    def __init__(self):
        super().__init__()
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.result = None

    def run(self):
        # simulate some work
        import time
        time.sleep(2)

        # store result and wake up whoever is waiting
        self.mutex.lock()
        self.result = "hello from thread(run)"
        self.condition.wakeAll()
        self.mutex.unlock()

    def get_result(self):
        self.mutex.lock()
        if self.result is None:
            self.condition.wait(self.mutex)  # releases lock and sleeps atomically
        value = self.result
        self.mutex.unlock()
        return value


w_t1 = WorkTH()
w_t1.start()

print("waiting for result...")
print(w_t1.get_result())   # blocks here until run() calls wakeAll()
print("done")
