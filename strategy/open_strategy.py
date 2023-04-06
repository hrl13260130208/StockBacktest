import math
from decimal import Decimal
from strategy.pair import PairStrategy
from common.option import Option, Record, PairRecord
from utils import calculator
from utils.slip import SlipPrice
from utils.generator import IDGenerator


# ====================================
#   开盘买卖策略
#       双数买，单数卖
# ====================================
class OpenStrategy(PairStrategy):

    def __init__(self, manager,logs):
        super().__init__(manager,logs)
        self.id = IDGenerator()

        self.current_buy = []
        self.current_sell = []
        self.slip = SlipPrice()

        self.could_buy = False
        self.could_sell = False

        self.max_price = -1
        self.min_price = 10

        self.num = 2000
        self.diff = 5

    def open(self, date, open):

        # if date == "20220627":
        #     print("----------")

        open = int(open * 100)

        for b in self.buy_prices.keys():
            op = self.buy_prices[b].grid_option.pair_option
            op.source = 1
            op.source_object = self.buy_prices[b]
            self.sell_options.append(op)

        for s in self.sell_prices.keys():
            op = self.sell_prices[s].grid_option.pair_option
            op.source = 1
            op.source_object = self.sell_prices[s]
            self.buy_options.append(op)

        bop = Option()
        bop.grid = open - int(math.ceil(self.diff / 2))
        bop.num = self.num
        bop.source = 2
        self.buy_options.append(bop)

        sop = Option()
        sop.grid = open + int(self.diff / 2)
        sop.num = self.num
        sop.source = 2
        self.sell_options.append(sop)

        bop.pair_option = sop
        sop.pair_option = bop

        self.buy_options = sorted(self.buy_options, key=lambda x: x.grid, reverse=True)
        self.sell_options = sorted(self.sell_options, key=lambda x: x.grid)

        smax = self.slip.max_price() * 100 - 40
        smin = self.slip.min_price() * 100 + 40
        if open > smax:
            self.could_buy = False
            self.could_sell = True
        elif open < smin:
            self.could_buy = True
            self.could_sell = False
        else:
            self.could_buy = True
            self.could_sell = True

    def deal(self, date, time, p):
        if p > self.max_price:
            self.max_price = p
        if p < self.min_price:
            self.min_price = p
        grid = int(p * 100)
        if self.buy_options and self.buy_options[0].grid > grid:
            #   低于且未买入，则买入
            opt: Option = self.buy_options[0]
            #   限制开盘价买入的交易，当股价过高的时候，先卖在买
            if opt.source == 2:
                if not self.could_buy:
                    return
            price = Decimal(str(opt.grid)) / Decimal("100")

            done = self.manager.buy(date, time, price, opt.num)

            if done:
                if opt.source == 2:
                    self.could_sell = True
                record = Record()
                record.id = self.id.next()
                record.price = price
                record.num = opt.num
                record.type = 1
                record.date = date
                record.time = time
                record.grid_option = opt
                record.real_amount = calculator.count_real_amount(price=price, num=opt.num, type=1)
                record.strategy = "OpenStrategy"
                del self.buy_options[0]
                # 判断是否是匹配交易
                if opt.source == 1:
                    self.add_pair(record,self.sell_prices[opt.source_object.id])
                    # pair = PairRecord()
                    # pair.set_buy(record)
                    # pair.set_sell(self.sell_prices[opt.source_object.id])
                    # self.pairs.append(pair)
                    del self.sell_prices[opt.source_object.id]
                else:
                    self.buy_prices[record.id] = record
                    self.current_buy.append(record.id)

        else:
            #   单数且未卖出，则卖出
            if self.sell_options and self.sell_options[0].grid < grid:
                opt = self.sell_options[0]
                price = Decimal(str(opt.grid)) / Decimal("100")

                #   限制开盘价买入的交易，当股价过低的时候，先买在卖
                if opt.source == 2:
                    if not self.could_sell:
                        return
                done = self.manager.sell(date, time, price, opt.num)

                if done:

                    if opt.source == 2:
                        self.could_buy = True
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
                    record.strategy = "OpenStrategy"
                    del self.sell_options[0]
                    # 判断是否是匹配交易
                    if opt.source == 1:
                        self.add_pair(self.buy_prices[opt.source_object.id],record)
                        # pair = PairRecord()
                        # pair.set_buy(self.buy_prices[opt.source_object.id])
                        # pair.set_sell(record)
                        # self.pairs.append(pair)
                        del self.buy_prices[opt.source_object.id]
                    else:
                        self.sell_prices[record.id] = record
                        self.current_sell.append(record.id)

    def close(self, date, close):
        if len(self.current_buy) > 0 and len(self.current_sell) > 0:
            buy_id = self.current_buy[0]
            sell_id = self.current_sell[0]

            # pair = PairRecord()
            # pair.set_buy(self.buy_prices[buy_id])
            # pair.set_sell(self.sell_prices[sell_id])
            # self.pairs.append(pair)
            self.add_pair(self.buy_prices[buy_id],self.sell_prices[sell_id])
            del self.buy_prices[buy_id]
            del self.sell_prices[sell_id]

        self.current_buy = []
        self.current_sell = []
        self.buy_options = []
        self.sell_options = []

        self.slip.add_max(self.max_price)
        self.slip.add_min(self.min_price)
