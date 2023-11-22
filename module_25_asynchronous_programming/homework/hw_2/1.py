import time
from pathlib import Path
import requests
import threading
from threading import Lock

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'cats-thr'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

pool = threading.BoundedSemaphore(value=10)


def get_cat(idx: int) -> None:
    with pool:
        r = requests.get(URL)
        print(r.status_code)
        content = r.content
        write_to_disk(content, idx)


def write_to_disk(content: bytes, id: int) -> None:
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, 'wb') as f:
        f.write(content)


def get_all_cats():
    task_list = []
    for i in range(CATS_WE_WANT):
        thr = threading.Thread(target=get_cat, args=(i,), name=f'thr-{i}')
        task_list.append(thr)
        thr.start()

    return task_list


def main():
    start = time.time()
    res = get_all_cats()
    for i in res:
        i.join()
    finish = time.time()
    print(finish - start)
    print(len(res))


if __name__ == '__main__':
    main()

