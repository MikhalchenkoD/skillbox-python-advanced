import threading
import time
from queue import PriorityQueue

class Producer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Producer: Running")
        tasks = [
            (0, "Task(priority=0)."),
            (2, "Task(priority=2)."),
            (1, "Task(priority=1)."),
            (4, "Task(priority=4)."),
            (3, "Task(priority=3)."),
            (6, "Task(priority=6)."),
        ]

        for priority, task in tasks:
            self.queue.put((priority, task))
            time.sleep(0.5)

        print("Producer: Done")

class Consumer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Consumer: Running")
        while True:
            priority, task = self.queue.get()
            if task is None:
                self.queue.task_done()
                break
            print(f">{task}          sleep({priority * 0.1})")
            time.sleep(priority * 0.1)
            self.queue.task_done()

        print("Consumer: Done")

def main():
    queue = PriorityQueue()
    producer = Producer(queue)
    consumer = Consumer(queue)

    producer.start()
    consumer.start()

    producer.join()
    queue.put((None, None))  # Adding a sentinel value to signal the consumer to stop
    queue.join()
    consumer.join()

if __name__ == "__main__":
    main()
