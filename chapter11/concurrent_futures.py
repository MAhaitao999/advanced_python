from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED, FIRST_COMPLETED
from concurrent.futures import Future

# 未来对象, task的返回容器

# 线程池, 为什么要线程池
# 主线程中可以获取某一个线程的状态或者某一个任务的状态, 以及返回值.
# 当一个线程完成的时候我们主线程能立即知道.
# futures可以让多线程和多进程编码接口一致

import time


def get_html(times):
    time.sleep(times)
    print("got page {} success".format(times))
    return times


executor = ThreadPoolExecutor(max_workers=2)

# 通过submit函数提交执行的函数到线程池中, submit是立即返回
# task1 = executor.submit(get_html, (3))
# task2 = executor.submit(get_html, (2))

# 要获取已经成功的task的返回
urls = [3, 4, 5, 6, 7]
all_tasks = [executor.submit(get_html, (url)) for url in urls]
wait(all_tasks, return_when=FIRST_COMPLETED)
print("main")
# for future in as_completed(all_tasks):
#     data = future.result()
#     print("get {} page success".format(data))

# 通过executor获取已经完成的task
# for data in executor.map(get_html, urls):
#     print("get {} page".format(data))

# done方法用于判定某个任务是否完成
# print(task1.done())

# 任务如果已经完成或者正在执行, 是不能够cancel的
# print(task2.cancel())
# time.sleep(4)
# print(task1.done())

# result方法可以获取task的执行结果
# print(task1.result())
