# =========================
# 管理股票
#
# =========================
import copy
import json
from decimal import Decimal
from utils import calculator
from common.option import Option, Record, PairRecord


class StrategyManager():

    def __init__(self, logs):
        #   现金
        self.cash = Decimal(10 ** 5)
        #   持仓
        self.hold_num = 0
        #   费用
        self.cost = Decimal(0)

        self.logs = logs

    def buy(self, date, time, price, num):
        worth = calculator.count_worth(price, num)
        trade_cost = calculator.count_cost(price, num)
        if (self.cash > worth + trade_cost):
            self.cash = self.cash - worth - trade_cost
            self.hold_num += num
            self.cost += trade_cost
            # self.logs.buy_logs(date, time, price, num)
            return True
        else:
            return False

    def sell(self, date, time, price, num):
        worth = calculator.count_worth(price, num)
        trade_cost = calculator.count_cost(price, num) + calculator.count_tax(price, num)
        if self.hold_num >= num:
            self.cash = self.cash + worth - trade_cost
            self.hold_num -= num
            self.cost += trade_cost
            # self.logs.sell_logs(date, time, price, num)
            return True
        else:
            return False

    # def print_logs(self, print_detail=False):
    #     print(f"现金：{self.cash.quantize(Decimal('0.00'))},持仓：{self.hold_num},"
    #           f"持仓价值估算：{self.hold_num * 5.5}，资产估值：{self.cash.quantize(Decimal('0.00')) + Decimal(self.hold_num) * Decimal('5.5')}，"
    #           f"交易费用：{self.cost.quantize(Decimal('0.00'))}")
    #     self.logs.print_logs(print_detail=print_detail)
    #     self.logs.generate_json()


class StockManger():

    def __init__(self, logs):
        self.managers = {}
        self.cash = Decimal("0")
        self.cash_map = {}
        self.logs = logs

    def register_manager(self, name, manager: StrategyManager):
        self.managers[name] = manager
        self.cash_map[name] = manager.cash
        self.cash += manager.cash

    def print_logs(self, print_detail=False):
        print("")
        print(f"现金：{self.cash.quantize(Decimal('0.00'))},持仓：{self.hold_num},"
              f"持仓价值估算：{self.hold_num * 5.5}，资产估值：{self.cash.quantize(Decimal('0.00')) + Decimal(self.hold_num) * Decimal('5.5')}，"
              f"交易费用：{self.cost.quantize(Decimal('0.00'))}")
        self.logs.print_logs(print_detail=print_detail)
        self.logs.generate_json()


# =========================
# 记录买卖日志
#
# =========================
class Logs():
    def __init__(self):
        self.pairs = []

        # 存储未匹配的交易
        self.buy_prices = []
        self.sell_prices = []

    def add_buy(self, buy):
        for k in buy.keys():
            self.buy_prices.append(buy[k])

    def add_sell(self, sell):
        for k in sell.keys():
            self.sell_prices.append(sell[k])

    def add_pair(self, buy: Record, sell: Record):
        pair = PairRecord()
        pair.set_buy(buy)
        pair.set_sell(sell)
        self.pairs.append(pair)

    def print_logs(self, print_detail=False):
        """
            打印交易详情
        :param print_detail:
        :return:
        """

        print(f"成对匹配交易:")
        pair_sum = 0
        for p in self.pairs:
            p: PairRecord
            if print_detail:
                print(p)
            pair_sum += p.profit()
        print(f"总计，匹配数量：{len(self.pairs)}，收益：{pair_sum}")

        print(f"未匹配买入交易：")

        buy_sum = 0
        for b in self.buy_prices:
            b: Record
            buy_sum += b.real_amount
            if print_detail:
                print(b)
        print(f"总计，交易数量：{len(self.buy_prices)} 总价：{buy_sum}")

        print(f"未匹配卖出交易:")

        sell_sum = 0
        for s in self.sell_prices:
            s: Record
            sell_sum += s.real_amount
            if print_detail:
                print(s)
        print(f"总计，交易数量：{len(self.sell_prices)} 总价：{sell_sum}")

        print(f"总交易数：{len(self.pairs) * 2 + len(self.buy_prices) + len(self.sell_prices)}")

    def generate_json(self):
        """
            生成json文件，用于网页展示交易
        :return:
        """
        markpoint = {}

        for p in self.pairs:
            p: PairRecord
            buy: Record = p.buy
            sell: Record = p.sell
            if buy.date in markpoint.keys():
                markpoint[buy.date].append([buy.date, buy.time, float(buy.price), buy.num, 1])
            else:
                markpoint[buy.date] = [[buy.date, buy.time, float(buy.price), buy.num, 1], ]

            if sell.date in markpoint.keys():
                markpoint[sell.date].append([sell.date, sell.time, float(sell.price), sell.num, 3])
            else:
                markpoint[sell.date] = [[sell.date, sell.time, float(sell.price), sell.num, 3], ]

        for buy in self.buy_prices:
            buy: Record

            if buy.date in markpoint.keys():
                markpoint[buy.date].append([buy.date, buy.time, float(buy.price), buy.num, 0])
            else:
                markpoint[buy.date] = [[buy.date, buy.time, float(buy.price), buy.num, 0], ]

        for sell in self.sell_prices:
            sell: Record
            if sell.date in markpoint.keys():
                markpoint[sell.date].append([sell.date, sell.time, float(sell.price), sell.num, 2])
            else:
                markpoint[sell.date] = [[sell.date, sell.time, float(sell.price), sell.num, 2], ]

        with open("data/logs/markpoint.json", "w", encoding="utf-8") as f:
            json.dump(markpoint, f)
