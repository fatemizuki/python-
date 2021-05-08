'''
程序的入口
'''

import os
import sys

# 添加解释器的环境变量（这个可以不用）

sys.path.append(
    os.path.dirname(__file__)
)

# 开始执行项目函数
from core import src

if __name__ == '__main__':
    # 1、先执行用户视图层
    src.run()
