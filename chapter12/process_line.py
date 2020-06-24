# with open('mydata.txt') as fp:
#     for line in iter(fp.readline, ''):
#         print(line[1])

# from functools import wraps
#
# def coroutine(func):
#     @wraps(func)
#     def primer(*args, **kwargs):
#         gen = func(*args, **kwargs)
#         next(gen)
#         return gen
#     return primer
#
# @coroutine
# def averager():
#     total = 0.0
#     count = 0
#     average = None
#     while True:
#         term = yield average
#         total += term
#         count += 1
#         average = total/count


# coro_avg = averager()
# from inspect import getgeneratorstate
# print(getgeneratorstate(coro_avg))
# print(coro_avg.send(10))
# print(coro_avg.send(20))
# print(coro_avg.send(30))
# print(coro_avg.send('spam'))

# class DemoException(Exception):
#     """
#     为这次演示定义的异常类型
#     """





# exc_coro = demo_exc_handling()
# next(exc_coro)
# exc_coro.send(11)
# exc_coro.send(22)
# exc_coro.close()
# from inspect import getgeneratorstate
# print(getgeneratorstate(exc_coro))


# class DemoException(Exception):
#     """
#     为这次演示定义的异常类型
#     """
#
#
# def demo_finally():
#     print('-> coroutine started')
#     try:
#         while True:
#             try:
#                 x = yield
#             except DemoException:
#                 print('*** DemoException handled. Continuing...')
#             else:
#                 print('-> coroutine received: {!r}'.format(x))
#     finally:
#         print('-> coroutine ending')



# from collections import namedtuple
#
# Result = namedtuple('Result', 'count average')
#
#
# def averager():
#     total = 0.0
#     count = 0
#     average = None
#     while True:
#         term = yield
#         if term is None:
#             break
#         total += term
#         count += 1
#         average = total/count
#     return Result(count, average)
#
#
# coro_avg = averager()
# print(next(coro_avg))
# coro_avg.send(10)
# coro_avg.send(30)
# coro_avg.send(6.5)
# try:
#     coro_avg.send(None)
# except StopIteration as exc:
#     result = exc.value
#
# print(result)
#
# from flask import Flask

# app = Flask(__name__)
#
# app.run()


from collections import namedtuple

Result = namedtuple('Result', 'count average')

# 子生成器
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
        return Result(count, average)


# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from averager()


# 客户端代码, 即调用方
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)  # 重要

    # print(results) # 如果要调试, 去掉注释
    report(results)


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

if __name__ == '__main__':
    main(data)








