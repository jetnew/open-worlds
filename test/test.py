import threading
import time

stop = False

class Server:
    def __init__(self, s):
        global stop
        while not stop:
            print(s)
            time.sleep(1)

def fn(s):
    global _lock
    _lock = threading.Lock()
    with _lock:
        Server(s)



t1 = threading.Thread(target=fn, args=('1',))
t1.start()

t2 = threading.Thread(target=fn, args=('2',))
t2.start()


time.sleep(5)
stop = True

t1.join()
t2.join()