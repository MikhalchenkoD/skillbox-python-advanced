import time
from pathlib import Path
import requests
import multiprocessing

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'cats-pr'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

semaphore = multiprocessing.Semaphore(10)


def get_cat(idx: int, s) -> None:
    with s:
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
        pr = multiprocessing.Process(target=get_cat, args=(i, semaphore), name=f'pr-{i}')
        task_list.append(pr)
        pr.start()

    return task_list


def main():
    start = time.time()
    res = get_all_cats()
    for i in res:
        i.join()
    finish = time.time()
    print(finish-start)
    print(len(res))


if __name__ == '__main__':
    main()
