

from data_generator import TradePrice



#====================================
#   观察者
#       负责监视股价变化，并通知策略
#====================================
class Observer():
    def __init__(self):
        self.strategys=[]
        self.generator = TradePrice()

    def add_strategy(self,strategy):
        self.strategys.append(strategy)

    def run(self,date):
        prices =self.generator.trade_price(date)
        if prices!=None:
            for strategy in self.strategys:
                strategy.do_open(date,prices[0][1])
                for p in prices:
                    strategy.do_deal(date, p[0], p[1])
                strategy.do_close(date,prices[-1][1])


    def finish(self):
        for strategy in self.strategys:
            strategy.finish()
