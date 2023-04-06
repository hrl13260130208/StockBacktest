from strategy.pair import PairStrategy
import math
from decimal import Decimal
from common.option import Option, Record, PairRecord
from common.grid import Grid
from utils import calculator
from utils.generator import IDGenerator
import json



# ====================================
#   网格交易策略
#       下跌差值买入，上涨差值卖出
# ====================================
class GridStrategy(PairStrategy):

    def __init__(self, manager,logs,config):
        super().__init__(manager,logs,config)
        self.id = IDGenerator()

        self.grid = Grid()

        # self.pairs = []

        # self.buy_prices = {}
        # self.sell_prices = {}
        #
        # self.buy_options = []
        # self.sell_options = []

        self.diff = self.grid.step + 1

    def open(self, date, open):
        self.update_option()


    def update_option(self):
        self.buy_options =[]
        self.sell_options =[]


        buy = self.grid.buy_grid
        for k in buy.keys():
            self.buy_options.append(buy[k])
        sell = self.grid.sell_grid
        for k in sell.keys():
            self.sell_options.append(sell[k])

        self.buy_options = sorted(self.buy_options, key=lambda x: x.grid, reverse=True)
        self.sell_options = sorted(self.sell_options, key=lambda x: x.grid)

    def deal(self, date, time, p):
        grid = int(p * 100)
        if self.buy_options and self.buy_options[0].grid > grid:
            #   低于且未买入，则买入
            opt: Option = self.buy_options[0]
            # 按网格价买入
            price = Decimal(str(opt.grid)) / Decimal("100")
            # 按当前价买入
            # price = Decimal(str(p))

            done = self.manager.buy(date, time, price, opt.num)

            if done:
                # print(f"买入：{date} {time} {price} {opt.num} {self.manager.cash} {self.manager.hold_num}")
                record = Record()
                record.id = self.id.next()
                record.price = price
                record.num = opt.num
                record.type = 1
                record.date = date
                record.time = time
                record.grid_option = opt
                record.real_amount = calculator.count_real_amount(price=price, num=opt.num, type=1)
                record.strategy="GridStrategy"

                # del self.buy_options[0]

                self.grid.del_buy(opt.grid)
                opt.record = record
                self.grid.add_sell(opt.grid + self.diff, opt)
                self.buy_prices[record.id] = record

                self.update_option()


        else:
            #   单数且未卖出，则卖出
            if self.sell_options and self.sell_options[0].grid < grid:
                opt: Option = self.sell_options[0]
                price = Decimal(str(opt.grid)) / Decimal("100")
                # 按当前价卖出
                # price = Decimal(str(p))
                done = self.manager.sell(date, time, price, opt.num)

                if done:
                    # print(f"卖出：{date} {time} {price} { opt.num} {self.manager.cash} {self.manager.hold_num}")
                    record = Record()
                    record.id = self.id.next()
                    record.price = price
                    record.num = opt.num
                    record.type = 2
                    record.date = date
                    record.time = time
                    record.grid_option = opt
                    record.real_amount = calculator.count_real_amount(price=price, num=opt.num, type=2)
                    record.strategy = "GridStrategy"
                    # del self.sell_options[0]

                    self.grid.del_sell(opt.grid)
                    self.grid.add_buy(opt.grid - self.diff)

                    self.add_pair(opt.get_pair_record(),record)
                    # pair = PairRecord()
                    # pair.set_buy(opt.get_pair_record())
                    # pair.set_sell(record)
                    # self.pairs.append(pair)
                    del self.buy_prices[opt.get_pair_record().id]

                    self.update_option()

    def close(self, date, close):
        self.buy_options = []
        self.sell_options = []


