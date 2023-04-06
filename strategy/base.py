from stock import StrategyManager


# ====================================
# 策略
#   负责判断是否买入或卖出
# ====================================
class Base():

    def __init__(self, manager):
        self.manager: StrategyManager = manager

    def open(self, date, open):
        pass

    def deal(self, date, time, p):
        pass

    def close(self, date, close):
        pass
    def do_open(self, date, open):
        pass

    def do_deal(self, date, time, p):
        pass

    def do_close(self, date, close):
        pass
    def finish(self):
        pass






