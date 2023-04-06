


class SlipPrice():

    def __init__(self,size=30):
        self.size = size
        self.max_prices=[6.3,]
        self.min_prices=[5,]


    def add_max(self,price):
        self.max_prices.append(price)

    def add_min(self,price):
        self.min_prices.append(price)

    def max_price(self):
        return max(self.max_prices[-self.size:])

    def min_price(self):
        return min(self.min_prices[-self.size:])






