from decimal import Decimal


def count_worth(price, num):
    """
        计算价值
    :param price:
    :param num:
    :return:
    """
    return Decimal(str(price)) * Decimal(str(num))


def count_cost(price, num):
    """
        计算手续费
    :param price:
    :param num:
    :return:
    """
    return max(count_worth(price, num) * Decimal("0.00004"), Decimal(5))


def count_tax(price, num):
    """
        计算税
    :param price:
    :param num:
    :return:
    """
    return (count_worth(price, num) * Decimal("0.001"))


def count_real_amount(price, num, type=1):
    """

    :param price:
    :param num:
    :param type: 类型 ：1 买入 2 卖出
    :return:
    """
    if type == 1:
        return count_worth(price, num) + count_cost(price, num)
    else:
        return count_worth(price, num) - count_cost(price, num) - count_tax(price, num)
