import json
from strategy.base import Base
from common.option import Option, Record, PairRecord


# ==============================
#   成对匹配交易策略
# ==============================
class PairStrategy(Base):

    def __init__(self, manager, logs):
        super(PairStrategy, self).__init__(manager)

        self.logs = logs
        # # 存储匹配的交易
        # self.pairs = []

        # 存储未匹配的交易
        self.buy_prices = {}
        self.sell_prices = {}

        # 存储待交易
        self.buy_options = []
        self.sell_options = []

    def clear_options(self):
        self.buy_options = []
        self.sell_options = []

    def add_buy_option(self, option):
        self.buy_options.append(option)

    def add_sell_option(self, option):
        self.sell_options.append(option)

    def del_buy_option(self, index):
        del self.buy_options[index]

    def del_sell_option(self, index):
        del self.sell_options[index]

    def add_buy_record(self, option: Option, record: Record):
        self.buy_prices[option] = record

    def add_sell_record(self, option: Option, record: Record):
        self.sell_prices[option] = record

    def del_buy_record(self, option: Option):
        del self.buy_prices[option]

    def del_sell_record(self, option: Option):
        del self.sell_prices[option]

    def add_pair(self, buy: Record, sell: Record):
        self.logs.add_pair(buy,sell)

    def set_buys(self):
        self.logs.add_buy(self.buy_prices)

    def set_sells(self):
        self.logs.add_sell(self.sell_prices)

    def finish(self):

        self.set_buys()
        self.set_sells()
    # def print_logs(self, print_detail=False):
    #     """
    #         打印交易详情
    #     :param print_detail:
    #     :return:
    #     """
    #
    #     print(f"成对匹配交易:")
    #     pair_sum = 0
    #     for p in self.pairs:
    #         p: PairRecord
    #         if print_detail:
    #             print(p)
    #         pair_sum += p.profit()
    #     print(f"总计，匹配数量：{len(self.pairs)}，收益：{pair_sum}")
    #
    #     print(f"未匹配买入交易：")
    #     buy_keys = self.buy_prices.keys()
    #     buy_sum = 0
    #     for key in buy_keys:
    #         b: Record = self.buy_prices[key]
    #         buy_sum += b.real_amount
    #         if print_detail:
    #             print(b)
    #     print(f"总计，交易数量：{len(buy_keys)} 总价：{buy_sum}")
    #
    #     print(f"未匹配卖出交易:")
    #     sell_keys = self.sell_prices.keys()
    #     sell_sum = 0
    #     for key in sell_keys:
    #         s: Record = self.sell_prices[key]
    #         sell_sum += s.real_amount
    #         if print_detail:
    #             print(s)
    #     print(f"总计，交易数量：{len(sell_keys)} 总价：{sell_sum}")
    #
    #     print(f"总交易数：{len(self.pairs) * 2 + len(buy_keys) + len(sell_keys)}")
    #
    # def generate_json(self):
    #     """
    #         生成json文件，用于网页展示交易
    #     :return:
    #     """
    #     markpoint = {}
    #
    #     for p in self.pairs:
    #         p: PairRecord
    #         buy: Record = p.buy
    #         sell: Record = p.sell
    #         if buy.date in markpoint.keys():
    #             markpoint[buy.date].append([buy.date, buy.time, float(buy.price), buy.num, 1])
    #         else:
    #             markpoint[buy.date] = [[buy.date, buy.time, float(buy.price), buy.num, 1], ]
    #
    #         if sell.date in markpoint.keys():
    #             markpoint[sell.date].append([sell.date, sell.time, float(sell.price), sell.num, 3])
    #         else:
    #             markpoint[sell.date] = [[sell.date, sell.time, float(sell.price), sell.num, 3], ]
    #
    #     buy_keys = self.buy_prices.keys()
    #
    #     for key in buy_keys:
    #         buy: Record = self.buy_prices[key]
    #
    #         if buy.date in markpoint.keys():
    #             markpoint[buy.date].append([buy.date, buy.time, float(buy.price), buy.num, 0])
    #         else:
    #             markpoint[buy.date] = [[buy.date, buy.time, float(buy.price), buy.num, 0], ]
    #
    #     sell_keys = self.sell_prices.keys()
    #     for key in sell_keys:
    #         sell: Record = self.sell_prices[key]
    #         if sell.date in markpoint.keys():
    #             markpoint[sell.date].append([sell.date, sell.time, float(sell.price), sell.num, 2])
    #         else:
    #             markpoint[sell.date] = [[sell.date, sell.time, float(sell.price), sell.num, 2], ]
    #
    #     with open("data/logs/markpoint.json", "w", encoding="utf-8") as f:
    #         json.dump(markpoint, f)
