# 通过queue的方式进行线程间同步
from queue import Queue
import time
import threading


def get_detail_html(queue):
    # 爬取文章详情页
    while True:
        url = queue.get() # 如果queue为空, 会阻塞在这里. queue本身是线程安全的.
        print("get detail html started")
        time.sleep(2)
        print("get detail html end")


def get_detail_url(queue):
    # 爬取文章列表页
    while True:
        print("get detail url started")
        time.sleep(4)
        for i in range(20):
            queue.put("http://projectsedu.com/{id}".format(id=i))
        print("get detailed url end")

# 1. 线程间通信方式——共享变量


if __name__ == "__main__":
    detail_url_queue = Queue(maxsize=1000)
    thread_detail_url = threading.Thread(target=get_detail_url, args=(detail_url_queue,))
    for i in range(10):
        html_thread = threading.Thread(target=get_detail_html, args=(detail_url_queue,))
        html_thread.start()

    start_time = time.time()

    detail_url_queue.task_done()
    detail_url_queue.join()
    print("last time: {}".format(time.time() - start_time))


"""
`queue`模块中有`Queue`类, `LifoQueue`, `PriorityQueue`都继承了`Queue`.

- maxsize
`maxsize`是实例化`Queue`类时的一个参数, 默认为0
`Queue(maxsize=0)`可以控制队列中数据的容量

- put
`Queue.put(block=True, timeout=None)`
`block`用于设置是否阻塞, `timeout`用于设置阻塞时等待时长
`put_nowait() = put(block=False)`
阻塞
当队列满了之后, `put`就会阻塞, 一直等待队列不再满时向里面添加数据
不阻塞
当队列满了之后, 如果设置`put`不阻塞, 或者等待时长到了之后会报错:`queue.Full`

- get
`Queue.get(block=True, timeout=None)`
`get_nowait() = get(block=False)`
阻塞
当队列空了之后, `get`就会阻塞, 一直等待队列中有数据后再获取数据
不阻塞
当队列空了之后, 如果设置`get`不阻塞, 或者等待时长到了之后会报错：`_queue.Empty`

- full & empty
`Queue.empty()/Queue.full()`用于判断队列是否为空、满
尽量使用`qsize`代替

- qsize
`Queue.qsize()`用于获取队列中大致的数据量
注意: 在多线程的情况下不可靠
因为在获取`qsize`时, 其他线程可能又对队列进行操作了

- join
`join`会在队列存在未完成任务时阻塞，等待队列无未完成任务，需要配合`task_done`使用

- task_done
执行一次`put`会让未完成任务+1, 但是执行`get`并不会让未完成任务-1, 需要使用`task_done`让未完成任务-1, 否则`join`就无法判断
队列为空时执行会报错: `ValueError: task_done() called too many times`

示例:
import queue
import threading
import time


def q_put():
    for i in range(10):
        q.put('1')
    while True:
        q.put('2')
        time.sleep(1)


def q_get():
    while True:
        temp = q.get()
        q.task_done()  # 可以理解为, 每task_done一次就从队列里删掉一个元素, 这样在最后join的时候根据队列长度是否为零来判断队列是否结束, 从而执行主线程
        print(temp)
        time.sleep(0.3)


q = queue.Queue()
t1 = threading.Thread(target=q_put)
t2 = threading.Thread(target=q_get)
t1.start()
t2.start()
q.join()
print('queue is empty now')

主线程执行到`q.join`就开始阻塞, 当`t2`线程将队列中的数据全部取出之后, 主线程才继续执行.
如果将`task_done`注释掉主线程就永远阻塞在`q.join`, 不再继续向下执行

生产者消费者模型(主要用于解耦)
在多线程开发当中, 如果生产线程处理速度很快, 而消费线程处理速度很慢, 那么生产线程就必须等待消费线程处理完, 才能继续生产数据.
同样的道理, 如果消费线程的处理能力大于生产线程, 那么消费线程就必须等待生产线程.
为了解决这个问题于是引入了生产者和消费者模式.
生产者消费者模式是通过一个容器来解决生产者和消费者的强耦合问题.
生产者和消费者彼此之间不直接通讯, 而通过阻塞队列来进行通讯, 所以生产者生产完数据之后不用等待消费者处理, 直接扔给阻塞队列, 消费者不找生产者要数据,
而是直接从阻塞队列里取, 阻塞队列就相当于一个缓冲区, 平衡了生产者和消费者的处理能力.

示例:
import threading
import time
import queue


def producer():
    count = 1
    while 1:
        q.put('No.%i' % count)
        print('Producer put No.%i' % count)
        time.sleep(1)
        count += 1


def customer(name):
    while 1:
        print('%s get %s' % (name, q.get()))
        time.sleep(1.5)


q = queue.Queue(maxsize=5)
p = threading.Thread(target=producer, )
c = threading.Thread(target=customer, args=('jack', ))
p.start()
c.start()
"""


