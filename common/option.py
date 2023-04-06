

# 网格交易待执行操作
class Option():

    #  网格位置 ： 价格*100
    grid=0
    # 数量
    num=0
    # 操作类型 1：买入 2 卖出
    option_type=0
    # 来源 ：  1 买卖配对交易 2 新增 3 网格交易
    source=0
    # source 为1时 设置对应的交易信息
    source_object=None
    # 匹配交易对应的网格操作（例如当前option是买入，pair_option存储的是卖出option）
    pair_option=None
    # 交易记录
    record=None

    def get_record(self):
        return self.record

    def get_pair_record(self):
        return self.pair_option.record

class Record():

    id = 0
    # 日期
    date = ""
    # 时间
    time = ""
    # 价格
    price = ""
    # 数量
    num = ""
    # 类型 ：  1：买入 2：卖出
    type = None
    # 实际发生金额
    real_amount=""
    # 网格操作
    grid_option=None

    strategy=None

    def __str__(self) -> str:
        return f"策略{self.strategy} {'买入' if self.type ==1 else '卖出'} {self.date} {self.time} {self.price}"


class PairRecord():

    def __init__(self):
        self.buy = None
        self.sell = None
        self.pair = False

        self.min_profit = 50

    def set_buy(self, record):
        self.buy = record

        self.pair = self.check_pair()

    def set_sell(self, record):
        self.sell = record

        self.pair = self.check_pair()

    def check_pair(self):

        if self.buy == None or self.sell == None:
            return False

        if self.buy.num != self.sell.num:
            raise ValueError("匹配交易的交易数据不同！")

        if abs(self.sell.real_amount) - abs(self.buy.real_amount) < 50:
            raise ValueError(f"匹配交易利润过低！交易详情：{self.__str__()}")

        return True

    def hold_record(self):
        if self.buy == None and self.sell == None:
            raise ValueError("买入与卖出记录都为空！")
        return self.buy if self.sell == None else self.sell

    def profit(self):
        if not self.check_pair():
            raise ValueError("交易未匹配！")

        return abs(self.sell.real_amount) - abs(self.buy.real_amount)

    def __str__(self) -> str:
        return f"{self.buy.__str__()}   {self.sell.__str__()}"
