from strategy.base import Base
import math
from decimal import Decimal
from common.option import Option, Record,PairRecord
from utils import calculator
from utils.generator import IDGenerator

# ====================================
#   滚动买卖策略
#       双数买，单数卖
# ====================================
class RollStrategy(Base):

    def __init__(self, manager):
        super().__init__(manager)

        self.buy_prices = set()
        self.sell_prices = set()

        self.num = 2000

    def deal(self, date, time, p):
        grid = int(p * 100)
        if grid % 2 == 0:
            #   双数且未买入，则买入
            if grid not in self.buy_prices:
                self.manager.buy(date, time, p, self.num)
                self.buy_prices.add(grid)
                #   买卖成对匹配，移除买入卖出列表
                pair = grid + 5
                if pair in self.sell_prices:
                    self.sell_prices.remove(pair)
                    self.buy_prices.remove(grid)
        else:
            #   单数且未卖出，则卖出
            if grid not in self.sell_prices:
                self.manager.sell(date, time, p, self.num)
                self.sell_prices.add(grid)
                #   买卖成对匹配，移除买入卖出列表
                pair = grid - 5
                if pair in self.buy_prices:
                    self.buy_prices.remove(pair)
                    self.sell_prices.remove(grid)
