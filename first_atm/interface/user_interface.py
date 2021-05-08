'''
逻辑接口层
    用户接口
'''
from db import db_handler
from lib import common

user_logger = common.get_logger('')


# 注册接口
def register_interface(username, password, balance=15000):
    # 判断用户是否存在,返回的是数据字典或None
    user_dic = db_handler.select(username)
    if user_dic:
        return False, '用户已存在'

    # 密码加密
    password = common.get_pwd_md5(password)

    user_dic = {
        'username': username,
        'password': password,
        'balance': balance,
        # 用于记录用户流水的列表
        'flow': [],
        # 用于记录用户购物车
        'shop_car': {},
        # locked: 用于记录用户是否被冻结
        'locked': False
    }

    db_handler.save(user_dic)

    msg = f'{username},注册成功'

    user_logger.info(msg)

    return True, msg


# 登录接口
def login_interface(username, password):
    user_dic = db_handler.select(username)

    if user_dic:

        if user_dic['locked']:
            return False, f'用户{username}账户已冻结'

        password = common.get_pwd_md5(password)

        if password == user_dic.get('password'):

            return True, f'{username},登录成功'
        else:
            return False, '密码错误'
    else:
        return False, '用户不存在，请重新输入'


# 余额接口
def check_bal_interface(username):
    user_dic = db_handler.select(username)

    return user_dic.get('balance')


# 改变额度接口
def change_balance_interface(username, balance):
    user_dic = db_handler.select(username)

    if user_dic:
        user_dic['balance'] = float(balance)

        # 记录流水
        flow = f'{username}修改额度为{balance}成功'
        user_dic['flow'].append(flow)

        db_handler.save(user_dic)

        return True, flow
    return False, '该账户不存在'


# 冻结账户接口
def change_lock_interface(username):
    user_dic = db_handler.select(username)

    if user_dic:
        user_dic['locked'] = True
        db_handler.save(user_dic)

        return True, f'账户{username}冻结成功'

    return False, '该用户不存在'
