import random
import collections
import queue
import argparse

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERAVAL = 5


# time 是事件发生的仿真时间，proc 是出租车进程实例的编号，action是描述活动的字符串
Event = collections.namedtuple('Event', ['time', 'proc', 'action'])


# 开始 出租车进程
# 每辆出租车调用一次taxi_process 函数，创建一个生成器对象，表示各辆出租车的运营过程。
def taxi_process(ident, trips, start_time=0):
    """
    每次状态变化时向创建事件，把控制权交给仿真器
    :param ident: 出租车编号
    :param trips: 出租车回家前的行程数量,接客数
    :param start_time: 离开车库的时间
    :return:
    """
    time = yield Event(start_time, ident, 'leave garage')  # 产出的第一个Event
    for i in range(trips):  # 每次行程都会执行一遍这个代码块
        # 产出一个Event实例，表示拉到了乘客 协程在这里暂停 等待下一次send() 激活
        time = yield Event(time, ident, 'pick up passenger')
        # 产出一个Event实例，表示乘客下车 协程在这里暂停 等待下一次send() 激活
        time = yield Event(time, ident, 'drop off passenger')
    # 指定的行程数量完成后，for 循环结束，最后产出 'going home' 事件。协程最后一次暂停
    yield Event(time, ident, 'going home')
    # 协程执行到最后 抛出StopIteration 异常


def compute_duration(previous_action):
    """使用指数分布计算操作的耗时"""
    if previous_action in ['leave garage', 'drop off passenger']:
        # 新状态是四处徘徊
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        # 新状态是开始行程
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unkonw previous_action: %s' % previous_action)
    return int(random.expovariate(1 / interval)) + 1


# 开始仿真
class Simulator:

    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()  # 带优先级的队列 会按时间正向排序
        self.procs = dict(procs_map)  # 从获取的procs_map 参数中创建本地副本，为了不修改用户传入的值

    def run(self, end_time):
        """
        调度并显示事件，直到时间结束
        :param end_time:  结束时间 只需要指定一个参数
        :return:
        """
        # 调度各辆出租车的第一个事件
        for iden, proc in sorted(self.procs.items()):
            first_event = next(proc)  # 预激协程 并产出一个 Event 对象
            self.events.put(first_event)  # 把各个事件加到self.events 属性表示的 PriorityQueue对象中

        # 此次仿真的主循环
        sim_time = 0  # 把 sim_time 归0
        while sim_time < end_time:
            if self.events.empty():  # 事件全部完成后退出循环
                print('*** end of event ***')
                break
            current_event = self.events.get()  # 获取优先级最高(time 属性最小)的事件
            sim_time, proc_id, previous_action = current_event  # 更新 sim_time
            print('taxi:', proc_id, proc_id * '  ', current_event)
            active_proc = self.procs[proc_id]  # 从self.procs 字典中获取表示当前活动的出租车协程
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)  # 把计算得到的时间发送给出租车协程。协程会产出下一个事件，或者抛出 StopIteration
            except StopIteration:
                del self.procs[proc_id]  # 如果有异常 表示已经退出， 删除这个协程
            else:
                self.events.put(next_event)  # 如果没有异常，把next_event 加入到队列
        else:  # 如果超时 则走到这里
            msg = '*** end of simulation time: {} event pendding ***'
            print(msg.format(self.events.qsize()))


def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS, seed=None):
    """初始化随机生成器，构建过程，运行仿真程序"""
    if seed is not None:
        random.seed(seed)  # 获取可复现的结果
    # 构建taxis 字典。值是三个参数不同的生成器对象。
    taxis = {i: taxi_process(i, (i + 1) * 2, i * DEPARTURE_INTERAVAL)
             for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Taxi fleet simulator.')
    # parser.add_argument('-e', '--end-time', type=int,
    #                     default=DEFAULT_END_TIME,
    #                     help='simulation end time; default=%s' % DEFAULT_END_TIME)
    # parser.add_argument('-t', '--taxis', type=int,
    #                     default=DEFAULT_NUMBER_OF_TAXIS,
    #                     help='number of taxis running; default = %s' % DEFAULT_NUMBER_OF_TAXIS)
    # parser.add_argument('-s', '--seed', type=int, default=None,
    #                     help='random generator seed (for testing)')
    #
    # args = parser.parse_args()
    main()