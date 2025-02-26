
import threading
import time

loop_count = 100

def cpu_task():
    count = 0
    for i in range(10_000_000):
        count += i


def single_thread():
    start = time.time()
    for _ in range(loop_count):
        cpu_task()

    print("싱글 스레드 실행 시간 :", time.time() - start)


def multi_thread():
    start = time.time()
    threads = []
    for _ in range(loop_count):
        t = threading.Thread(target=cpu_task)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("멀티 스레드 실행 시간 :", time.time() - start)


# single_thread()
multi_thread()