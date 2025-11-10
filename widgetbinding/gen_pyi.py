# 相同的部分注释略

import logging
import argparse

import PySide6
import shiboken6  # type: ignore
import shiboken6_generator
from PySide6.QtCore import qVersion

# *** 这个案例用了PySide6, 先导入自己扩展里用到的库PySide6, 下面代码会同时加载
#     PySide6的动态链接库, 如果动态链接库没有提前载入, 我们自己用 屎啵啃6 生成的
#     绑定默认没有生成导入PySide6的代码, 需要注意模块导入顺序, 这里暂时没有研究
#     这个问题, 后续最好在包装的C Py 扩展里加上自定义的导入PySide6的代码.

# *** 相当于是说, 我们要先随便导入个 PySide6 模组, 让动态链接库先让 PySide6 自己
#     加载好, 再去导入我们的 Py C 模组
import PySide6.QtWidgets

from shibokensupport.signature.lib.pyi_generator import *  # type: ignore

print(f"PySide6.QtCore.{qVersion()=}")
print(f"{shiboken6.__version__=}")
print(f"{shiboken6_generator.__version__=}")

# --- 这个案例我们用了这几个, 写进去到时候会一起插入到pyi文件里
PySide6.__all__ = ["QtWidgets", "QtGui", "QtCore"]

parser = argparse.ArgumentParser()
options = parser.parse_args()
options._pyside_call = True

options.quiet = False
options.logger = logging.getLogger()

generate_pyi(  # type: ignore
    # *** generate_pyi 内部会尝试去 import wiggly
    "wiggly",
    ".",
    options=options,
)
print("ok.")
