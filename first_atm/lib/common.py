'''
公共方法
'''

import hashlib
from conf import settings
from logging import config, getLogger


# md5加密
def get_pwd_md5(password):
    md5_obj = hashlib.md5()
    md5_obj.update(password.encode('utf-8'))
    salt = 'taneda risa'
    md5_obj.update(salt.encode('utf-8'))

    return md5_obj.hexdigest()


# 登录认证装饰器

def login_auth(func):
    def inner(*args, **kwargs):
        from core import src
        if src.login_user:
            res = func(*args, **kwargs)
            return res
        else:
            print('未登陆')
            src.login()

    return inner


# 添加日志功能


def get_logger(log_type):
    config.dictConfig(
        settings.LOGGING_DIC
    )

    logger = getLogger(log_type)

    return logger