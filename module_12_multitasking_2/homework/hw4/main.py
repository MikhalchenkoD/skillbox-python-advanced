import requests
import time
from datetime import datetime
from threading import Thread, Lock
from queue import Queue

log_lock = Lock()
queue = Queue()

def get_current_timestamp(timestamp):
    response = requests.get(f"http://127.0.0.1:8080/timestamp/{timestamp}")
    if response.status_code == 200:
        return response.text
    else:
        return None

def write_log(timestamp, date):
    log_line = f"{timestamp} {date}"
    with log_lock:
        with open("logs.txt", "a") as file:
            file.write(log_line + "\n")

def worker():
    while True:
        timestamp = queue.get()
        if timestamp is None:
            break
        current_timestamp = time.time()
        date = get_current_timestamp(current_timestamp)
        if date is None:
            break
        write_log(current_timestamp, date)
        time.sleep(1)
        queue.task_done()

if __name__ == "__main__":
    start_timestamp = int(time.time())
    threads = []
    for i in range(10):
        queue.put(start_timestamp + i)

    for _ in range(10):
        t = Thread(target=worker)
        t.start()
        threads.append(t)

    queue.join()

    for _ in range(10):
        queue.put(None)

    for t in threads:
        t.join()
