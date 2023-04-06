import json
from strategy.base import Base
from common.config import Config
from common.option import Option, Record, PairRecord


# ==============================
#   成对匹配交易策略
# ==============================
class PairStrategy(Base):

    def __init__(self, manager, logs,config:Config):
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
        self.config = config

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

    def open(self, date, open):
        pass

    def deal(self, date, time, p):
        pass

    def close(self, date, close):
        pass
    def do_open(self, date, open):
        self.open(date,open)

    def do_deal(self, date, time, p):
        self.deal(date,time,p)

    def do_close(self, date, close):
        self.close(date,close)
        if self.config.hold:
            self.manager.add_hold_logs()
