# python3.3中新加了yield from语法
# from itertools import chain
#
# my_list = [1, 2, 3]
# my_dict = {
#     "bobby1": "http://projectedu.com",
#     "bobby2": "http://imooc.com",
# }
#
#
# def my_chain(*args, **kwargs):
#     for my_iterable in args:
#         yield from my_iterable
#         for value in my_iterable:
#             yield value
#
#
# for value in my_chain(my_list, my_dict, range(5, 10)):
#     print(value)

# # 子生成器
# def average_gen():
#     total = 0
#     count = 0
#     average = 0
#     while True:
#         new_num = yield average
#         count += 1
#         total += new_num
#         average = total/count
#
# # 委托生成器
# def proxy_gen():
#     while True:
#         yield from average_gen()
#
# # 调用方
# def main():
#     calc_average = proxy_gen()
#     next(calc_average)            # 预激下生成器
#     print(calc_average.send(10))  # 打印：10.0
#     print(calc_average.send(20))  # 打印：15.0
#     print(calc_average.send(30))  # 打印：20.0
#
# if __name__ == '__main__':
#     main()

import re
import reprlib
RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))


class ArithmeticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        result = type(self.begin + self.end)(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index


ap = ArithmeticProgression(0, 1/3, 3)
print(list(ap))
from fractions import Fraction
ap = ArithmeticProgression(0, Fraction(1, 3), 1)
print(list(ap))
from decimal import Decimal
ap = ArithmeticProgression(0, Decimal('.1'), .3)
print(list(ap))

import itertools
def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen

