from core import src
from interface import user_interface


def add_user():
    src.register()


def change_balance():
    while True:
        input_user = input('请输入要修改额度的用户').strip()
        input_balance = input('请输入要修改的额度').strip()

        if input_balance.isdigit():
            flag, msg = user_interface.change_balance_interface(input_user, input_balance)

            if flag:
                print(msg)
                break

            else:
                print(msg)

        else:
            print('请输入正确额度')


def lock_user():
    while True:
        input_user = input('请输入需要冻结的用户').strip()

        flag, msg = user_interface.change_lock_interface(input_user)

        if flag:
            print(msg)
            break

        else:
            print(msg)


admin_dic = {
    '1': add_user,
    '2': change_balance,
    '3': lock_user
}


def admin_run():
    while True:
        print('''
            1.添加账户
            2.修改额度
            3.冻结账户        
        ''')

        choice = input('请选择功能').strip()

        if choice not in admin_dic:
            print('请输入正确编号')
            continue

        admin_dic.get(choice)()
