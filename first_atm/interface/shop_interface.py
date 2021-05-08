'''
逻辑接口层
    购物商城接口
'''

from db import db_handler


# 调用商品支付接口
def shopping_interface(username, shopping_car):
    # 计算消费总额
    cost = 0

    for price, value in shopping_car.values():
        cost += (price * value)

    from interface import bank_interface
    flag = bank_interface.pay_interface(username, cost)

    if flag:
        return True, '支付成功，即将发货'
    return False, '支付失败，金额不足'


# 购物车添加接口
def add_shopping_car_interface(username, shopping_car):
    # 获取当前用户已有的购物车
    user_dic = db_handler.select(username)

    user_shop_car = user_dic.get('shop_car')

    for shop_name, price_value in shopping_car.items():
        if shop_name in user_shop_car:
            user_dic['shop_car'][shop_name][1] += price_value[1]

        else:
            user_dic['shop_car'].update(
                {shop_name: price_value}
            )

    db_handler.save(user_dic)

    return True, '添加购物车成功'


# 查看购物车接口

def check_shopping_car_interface(username):
    user_dic = db_handler.select(username)

    return user_dic.get('shop_car')
