'''
数据处理层
'''

import json
import os
from conf import settings

# 查看数据
def select(username):

    # 1.接收接口层传来的username，拼接成json路径
    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{username}.json'
    )

    # 2.校验user的json路径是否存在
    if os.path.exists(user_path):

        # 3. 存在则返回给接口层
        with open(user_path, mode='rt', encoding='utf-8') as f:

            user_dic = json.load(f)
            return user_dic

    # 3. 不return，默认return None

# 保存数据
def save(user_dic):

    # 1.拼接用户字典
    username = user_dic.get('username')

    user_path = os.path.join(
        settings.USER_DATA_PATH, f'{username}.json'
    )

    # 2.保存用户数据
    # 文件名：用户名.json
    with open(user_path, mode='wt', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)
