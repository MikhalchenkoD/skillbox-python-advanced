from threading import Semaphore, Thread
import time
import signal

sem: Semaphore = Semaphore()
exit_flag = False  # Флаг для выхода из цикла


def fun1():
    global exit_flag
    while not exit_flag:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    global exit_flag
    while not exit_flag:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


def handle_interrupt(signum, frame):
    global exit_flag
    exit_flag = True
    print('\nReceived keyboard interrupt, quitting threads.')


t1: Thread = Thread(target=fun1)
t2: Thread = Thread(target=fun2)
signal.signal(signal.SIGINT, handle_interrupt)
t1.start()
t2.start()

t1.join()
t2.join()
