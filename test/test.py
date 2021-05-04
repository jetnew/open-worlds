import threading
import time

stop = False

def fn(s):
    global n, _lock
    with _lock:
        while not stop:
            print(s)
            time.sleep(1)

_lock = threading.Lock()

t1 = threading.Thread(target=fn, args=('1',))
t1.start()

t2 = threading.Thread(target=fn, args=('2',))
t2.start()


time.sleep(10)
stop = True

t1.join()
t2.join()