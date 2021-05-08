'''
用户视图层
'''

from interface import user_interface
from interface import bank_interface
from interface import shop_interface
from lib import common

login_user = None

# 1、注册功能
# 面条版
'''
def register():
    while True:
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()

        if password == re_password:
            import json
            import os
            from conf import settings

            user_path = os.path.join(
                settings.USER_DATA_PATH, f'{username}.json'
            )

            # 判断用户是否存在
            if os.path.exists(user_path):
                with open(user_path, mode='rt', encoding='utf-8') as f:
                    json.load(f)

                if user_path:
                    print('用户已存在，请重新输入')
                    continue

            # 不存在则创建
            user_dic = {
                'username': username,
                'password': password,
                'balance': 15000,
                # 用于记录用户流水的列表
                'flow': [],
                # 用于记录用户购物车
                'shop_car': {},
                # locked: 用于记录用户是否被冻结
                'locked': False
            }


            # 文件名：用户名.json
            with open(user_path, mode='wt', encoding='utf-8') as f:
                json.dump(user_dic, f, ensure_ascii= False)
'''


# 分层版
def register():
    while True:
        username = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('请确认密码：').strip()

        if password == re_password:

            # 调用接口层的数据接口，把用户名和密码交给接口层进行处理
            flag, msg = user_interface.register_interface(username, password)

            # 根据flag判断注册是否成功，判断程序是否退出
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('请确保两次密码相同')
            continue


# 2、登录功能
def login():
    while True:
        username = input('输入用户名：').strip()
        password = input('输入密码：').strip()

        flag, msg = user_interface.login_interface(username, password)

        if flag:
            global login_user
            login_user = username
            print(msg)
            break
        else:
            print(msg)


# 3、查看余额
@common.login_auth
def check_balance():
    balance = user_interface.check_bal_interface(login_user)

    print(f'{login_user}余额为{balance}')


# 4、提现功能
@common.login_auth
def withdraw():
    while True:
        input_money = input('请输入提现金额').strip()
        if not input_money.isdigit():
            print('请输入数字')
            continue

        flag, msg = bank_interface.withdraw_interface(
            login_user, input_money
        )

        if flag:
            print(msg)
            break
        else:
            print(msg)


# 5、还款功能
@common.login_auth
def repay():
    while True:
        input_money = input('请输入还款金额').strip()

        if not input_money.isdigit():
            print('请输入正确的金额')
            continue

        input_money = float(input_money)

        if input_money > 0:
            flag, msg = bank_interface.repay_interface(
                login_user, input_money
            )

            if flag:
                print(msg)
                break

        else:
            print('输入的金额不能小于零')
            continue


# 6、转账功能
@common.login_auth
def transfer():
    # 1.需要转账的账户
    # 2.需要转账的金额
    while True:
        input_money = input('请输入转账金额').strip()
        input_user = input('请输入转账账户').strip()

        if not input_money.isdigit():
            print('请输入正确的金额')
            continue

        input_money = float(input_money)

        if input_money > 0:

            flag, msg = bank_interface.transfer_interface(
                login_user, input_user, input_money
            )

            if flag:
                print(msg)
                break
            else:
                print(msg)

        else:
            print('请输入大于0的金额')


# 7、查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_bank_interface(login_user)

    if flow_list:
        for i in flow_list:
            print(i)
    else:
        print('该用户没有流水')


# 8、购物功能
@common.login_auth
def shopping():
    # 1.创建一个商品列表
    shop_list = [
        ['taneda', 100],
        ['risa', 200],
        ['touyama', 300],
        ['nao', 400],
    ]

    # 初始化当前购物车
    shopping_car = {}  # {'商品名称': [单价, 数量]}

    while True:
        # 2.1 打印商品信息，让顾客挑选
        print('=================================')
        for list, shop in enumerate(shop_list):  # 枚举，返回索引下标和值
            shop_name, shop_price = shop
            print(f'{list}号商品{shop_name}，价格为{shop_price}')
        print('=================================')

        choice = input('请输入商品编号(是否进入结算y or n)').strip()

        if choice == 'y':
            if not shopping_car:
                print('购物车为空')
                continue

            # 调用商品支付接口
            flag, msg = shop_interface.shopping_interface(login_user, shopping_car)

            if flag:
                print(msg)
                break
            else:
                print(msg)

        elif choice == 'n':
            if not shopping_car:
                print('购物车为空')
                continue

            # 调用添加购物车接口
            flag, msg = shop_interface.add_shopping_car_interface(login_user, shopping_car)

            if flag:
                print(msg)
                break

        if not choice.isdigit():
            print('请输入正确的编号')
            continue

        choice = int(choice)

        if choice not in range(len(shop_list)):
            print('请输入正确的编号')
            continue

        # 2.2 获取商品名称和单价
        shop_name, shop_price = shop_list[choice]

        # 2.3 加入购物车
        # 判断用户选择的商品是否重复，重复则加1
        if shop_name in shopping_car:
            shopping_car[shop_name][1] += 1


        else:
            shopping_car[shop_name] = [shop_price, 1]

        print('当前购物车', shopping_car)


# 9、查看购物车
@common.login_auth
def check_shop_car():
    shop_car = shop_interface.check_shopping_car_interface(login_user)

    print(shop_car)



# 10、管理员功能

@common.login_auth
def admin():
    from core import admin
    admin.admin_run()


# 创建函数功能字典
func_dic = {
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_car,
    '10': admin,
}


# 视图层主程序
def run():
    while True:
        print('''
        ======= atm + 购物车 =======
                1、注册功能
                2、登录功能
                3、查看余额
                4、提现功能
                5、还款功能
                6、转账功能
                7、查看流水
                8、购物功能
                9、查看购物车
                10、管理员功能
        ===========================
        ''')

        choice = input('请输入功能编号：').strip()

        if choice not in func_dic:
            print('请输入正确的功能编号')
            continue

        func_dic.get(choice)()  # func_dic.get('1')() --> register()
