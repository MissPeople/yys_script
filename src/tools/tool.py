import os
import sys


def get_resource_path(relative_path):
    """获取资源文件的绝对路径（兼容打包后环境）"""
    if getattr(sys, 'frozen', False):
        # 打包后的环境
        base_path = sys._MEIPASS
    else:
        # 开发环境（当前文件位于src/func/，根目录为yys_script/）
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    return os.path.join(base_path, relative_path)