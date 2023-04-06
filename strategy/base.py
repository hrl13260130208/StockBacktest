from stock import Manager


# ====================================
# 策略
#   负责判断是否买入或卖出
# ====================================
class Base():

    def __init__(self, manager):
        self.manager: Manager = manager

    def open(self, date, open):
        pass

    def deal(self, date, time, p):
        pass

    def close(self, date, close):
        pass

    def finish(self):
        pass






