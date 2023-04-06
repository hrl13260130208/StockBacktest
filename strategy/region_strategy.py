from strategy.base import Base


# ====================================
#   区间买卖策略
#       0-4 买入 5-9 卖出
# ====================================
class RegionStrategy(Base):

    def __init__(self, manager):
        super().__init__(manager)

        self.buy_prices = set()
        self.sell_prices = set()

        self.num = 2000

        self.options = {}

        for i in range(50):
            if i % 2 == 0:
                # 0-5 买入
                p = 500 + i * 5
                self.options[p] = 0
                self.options[p + 1] = 0
                self.options[p + 2] = 0
                self.options[p + 3] = 0
                self.options[p + 4] = 0
            else:
                # 0-5 买入
                p = 500 + i * 5
                self.options[p] = 1
                self.options[p + 1] = 1
                self.options[p + 2] = 1
                self.options[p + 3] = 1
                self.options[p + 4] = 1

    def deal(self, date, time, p):
        grid = int(p * 100)
        op = self.options[grid]
        if op == 0:
            #   双数且未买入，则买入
            if grid not in self.buy_prices:
                self.manager.buy(date,time, p, self.num)
                self.buy_prices.add(grid)
                #   买卖成对匹配，移除买入卖出列表
                pair = grid + 5
                if pair in self.sell_prices:
                    self.sell_prices.remove(pair)
                    self.buy_prices.remove(grid)
        else:
            #   单数且未卖出，则卖出
            if grid not in self.sell_prices:
                self.manager.sell(date, time,p, self.num)
                self.sell_prices.add(grid)
                #   买卖成对匹配，移除买入卖出列表
                pair = grid - 5
                if pair in self.buy_prices:
                    self.buy_prices.remove(pair)
                    self.sell_prices.remove(grid)


