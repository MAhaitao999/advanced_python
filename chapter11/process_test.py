from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor
import time
# 多进程编程
# 耗CPU的操作, 用多进程编程. 对于IO操作来说, 使用多线程编程. 进程切换代价要高于线程.

# 1. 对于耗费CPU的操作, 多进程优于多线程

def fib(n):
    if n < 2:
        return 1
    return fib(n-1) + fib(n-2)


# print(fib(3))

# with ThreadPoolExecutor(3) as executor:
# with ProcessPoolExecutor(3) as executor:
#     all_task = [executor.submit(fib, (num)) for num in range(25, 50)]
#     start_time = time.time()
#     for future in as_completed(all_task):
#         data = future.result()
#         print("exe result: {}".format(data))
#
#     print("last time is: {}".format(time.time() - start_time))

def random_sleep(n):
    time.sleep(n)
    return n


# with ThreadPoolExecutor(3) as executor:
with ProcessPoolExecutor(3) as executor:
    all_task = [executor.submit(random_sleep, (num)) for num in [2]*30]
    start_time = time.time()
    for future in as_completed(all_task):
        data = future.result()
        print("exe result: {}".format(data))

    print("last time is: {}".format(time.time() - start_time))