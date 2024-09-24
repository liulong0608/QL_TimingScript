# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         fn_print.py
# @author           Echo
# @EditTime         2024/9/24
from typing import *

all_print_list = []


def fn_print(*args, sep=' ', end='\n', **kwargs):
    global all_print_list
    output = ""
    # 构建输出字符串
    for index, arg in enumerate(args):
        if index == len(args) - 1:
            output += str(arg)
            continue
        output += str(arg) + sep
    output = output + end
    all_print_list.append(output)
    # 调用内置的 print 函数打印字符串
    print(*args, sep=sep, end=end, **kwargs)
