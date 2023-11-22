import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore, cv: threading.Condition) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.cv: threading.Condition = cv
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
                if TOTAL_TICKETS == 1:
                    with self.cv:
                        self.cv.notify_all()
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore, cv: threading.Condition) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.cv: threading.Condition = cv

    def run(self) -> None:
        global TOTAL_TICKETS
        while True:
            with self.cv:
                self.cv.wait()
                if TOTAL_TICKETS <= 1:
                    self.add_tickets()
                    with self.sem:
                        self.sem.release()

    def add_tickets(self) -> None:
        global TOTAL_TICKETS
        added_tickets = random.randint(1, 10)
        logger.info(f'Director added {added_tickets} tickets')
        TOTAL_TICKETS += added_tickets


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    condition_variable: threading.Condition = threading.Condition()
    sellers: List[Seller] = []
    for _ in range(3):
        seller = Seller(semaphore, condition_variable)
        seller.start()
        sellers.append(seller)

    director = Director(semaphore, condition_variable)
    director.start()

    for seller in sellers:
        seller.join()

    director.join()


if __name__ == '__main__':
    main()
