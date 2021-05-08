'''
逻辑接口层
    银行接口
'''
from db import db_handler


# 提现功能
def withdraw_interface(username, money):
    # 1.先获取用户字典
    user_dic = db_handler.select(username)

    # 2.判断用户金额是否足够
    balance = float(user_dic.get('balance'))
    money2 = float(money) * 1.05  # 手续费5%

    if balance >= money2:
        balance -= money2
        user_dic['balance'] = balance

        # 记录流水
        flow = f'{username}提现金额{money},手续费为{money2 - float(money)}'
        user_dic['flow'].append(flow)

        db_handler.save(user_dic)

        return True, flow

    return False, '提现金额不足，请重新输入'


# 还款功能
def repay_interface(username, money):
    user_dic = db_handler.select(username)

    user_dic['balance'] += money

    # 记录流水
    flow = f'{username},还款{money}成功'
    user_dic['flow'].append(flow)

    db_handler.save(user_dic)

    return True, flow


# 转账功能
def transfer_interface(login_user, to_user, money):
    # 获取当前用户和目标用户的字典

    login_user_dic = db_handler.select(login_user)
    to_user_dic = db_handler.select(to_user)

    # 判断目标用户是否存在

    if not to_user_dic:
        return False, '目标用户不存在'

    # 判断当前用户的余额是否足够

    if float(login_user_dic['balance']) >= money:
        login_user_dic['balance'] -= money
        to_user_dic['balance'] += money

        # 记录流水
        login_user_flow = f'转账给{to_user}{money}成功'
        to_user_flow = f'接收{login_user}{money}转账成功'

        login_user_dic['flow'].append(login_user_flow)
        to_user_dic['flow'].append(to_user_flow)

        db_handler.save(login_user_dic)
        db_handler.save(to_user_dic)

        return True, login_user_flow

    return False, '转账金额不足'


# 查看流水接口
def check_bank_interface(username):
    user_dic = db_handler.select(username)

    return user_dic['flow']


# 支付接口
def pay_interface(username, cost):
    user_dic = db_handler.select(username)

    if float(user_dic['balance']) >= float(cost):
        user_dic['balance'] -= float(cost)

        flow = f'用户{username}消费金额{cost}'

        user_dic['flow'].append(flow)

        db_handler.save(user_dic)

        return True

    return False
