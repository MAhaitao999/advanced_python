from threading import Lock, RLock # 可重入的锁

# 在同一个线程里面, 可以连续调用多次acquire, 一定要注意acquire的次数要和release的次数相等.
total = 0
lock = RLock()

def add():
    # 1. dosomething1
    # 2. io操作
    # 1. dosomething3
    global total
    global lock
    for i in range(100000):
        lock.acquire()
        total += 1
        lock.release()


def desc():
    global total
    for i in range(100000):
        lock.acquire()
        lock.acquire()
        total -= 1
        lock.release()
        lock.release()

import threading
thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(total)

#1. 用锁会影响性能
#2. 会引起死锁
# 死锁的情况 A(a, b)
"""
A(a, b)
acquire (a)
acquire (b)

B(a, b)
acquire (b)
acquire (a)
"""

"""
def add(lock):
    global total
    for i in range(100000):
        lock.acquire()
        dosomething(lock)
        total += 1
        lock.release()
        
def dosomething(lock):
    lock.acquire()
    # do something
    lock.release()
"""

# def add1(a):
#     a += 1
#
#
# def desc(a):
#     a -= 1

"""
add
1. load a
2. load 1
3. +
4. 赋值给a
"""

"""
desc
1. load a
2. load 1
3. -
4. 赋值给a
"""

# import dis
# print(dis.dis(add1))
# print(dis.dis(desc))
"""
0
 31           0 LOAD_FAST                0 (a)
              3 LOAD_CONST               1 (1)
              6 INPLACE_ADD
              7 STORE_FAST               0 (a)
             10 LOAD_CONST               0 (None)
             13 RETURN_VALUE
None
 35           0 LOAD_FAST                0 (a)
              3 LOAD_CONST               1 (1)
              6 INPLACE_SUBTRACT
              7 STORE_FAST               0 (a)
             10 LOAD_CONST               0 (None)
             13 RETURN_VALUE
None
"""