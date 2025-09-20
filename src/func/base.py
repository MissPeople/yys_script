import logging
import os
import random
import struct
from random import randint

import cv2
import numpy as np
import win32con
import win32gui

from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal
from adb_shell.adb_device import AdbDeviceTcp
from src.conf.config import config
from src.tools.tool import get_resource_path

screenshot_dir = get_resource_path('resource')

class Base(QThread):

    sendmsg = pyqtSignal(str)

    def __init__(self, quit_game_enable=1):
        super().__init__()
        port = config.general['adb_port']
        self.stop = True
        self.quit_game_enable = quit_game_enable
        self.device = AdbDeviceTcp("127.0.0.1", port, default_transport_timeout_s=5.)
        self.device.connect()
        output = self.device.shell("wm size").strip()
        size = output.split(": ")[-1]
        self.width,self.height = map(int, size.split("x"))
        self.x_top = self.y_top = self.x_bottom = self.y_bottom = 0
        self.res_path = '../resource'

    def open_image_list(self, pics):
        '''按目录层级打开相应的所有图片，并使用每个name作为key
            [
                [dir1, dir2, name1],
                [dir1, dir2, name2]
            ]
        '''
        ims = {}
        for onepath in pics:
            base_dir = screenshot_dir
            if onepath:
                key = onepath[-1]
                for relative in onepath:
                    base_dir = os.path.join(base_dir, relative)
                filepatch = base_dir + '.png'

                try:
                    im = Image.open(filepatch)
                    # logging.debug('打开图片：{0}'.format(filepatch))
                    # im.show()
                    ims[key] = im
                    # ims[key].show()
                except Exception as error:
                    logging.error('打开图片失败，{0}, msg:{1}'.format(filepatch, error))
        return ims

    def pil_to_cv2(self, pil_image):
        """将PIL图像转换为OpenCV格式"""
        img_np = np.array(pil_image)
        return cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)

    def tap(self, x: int, y: int):
        self.device.shell(f"input tap {x} {y}")

    def tapOther(self):
        tar_x = randint(int(self.width*0.95),self.width)
        tar_y = randint(int(self.height*0.25),int(self.height*0.75))
        self.device.shell(f"input tap {tar_x} {tar_y}")

    def screenshot(self):
        raw = self.device.shell("screencap", decode=False)  # 原始输出
        w, h, f = struct.unpack_from('<III', raw, 0)
        assert f == 1, "只支持 RGBA 格式"
        img = Image.frombuffer('RGBA', (w, h), raw[12:], 'raw', 'RGBA', 0, 1)
        return img

    def find_img(self, img_template_path, yys_script, threshold=0.8):
        """返回匹配区域内的随机点 (x, y)，找不到返回 None"""
        try:
            # 截图 → RGBA → BGR
            img_src = cv2.cvtColor(np.array(yys_script), cv2.COLOR_RGBA2BGR)

            # 模板 → BGR
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
            if img_template is None:
                return None

            # 模板匹配
            res = cv2.matchTemplate(img_src, img_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val >= threshold:
                h, w = img_template.shape[:2]
                # 计算匹配区域的边界
                left, top = max_loc
                right, bottom = left + w, top + h

                # 在匹配区域内生成随机点
                random_x = random.randint(left, right - 1)
                random_y = random.randint(top, bottom - 1)

                return (random_x, random_y)
            else:
                return None
        except Exception as e:
            return None

    def resize_win_size(self):
        handler = win32gui.FindWindow(0, config.general['win_name'])  # 获取窗口句柄
        self.x_top, self.y_top, self.x_bottom, self.y_bottom = \
            win32gui.GetWindowRect(handler)
        # self.win_width = self.x_bottom - self.x_top
        # self.win_height = self.y_bottom - self.y_top
        win32gui.SetWindowPos(handler, win32con.HWND_NOTOPMOST,
                                  self.x_top, self.y_top, 796, 488,
                                  win32con.SWP_SHOWWINDOW)

    def display_msg(self, msg):
        """输出日志到框内"""
        self.sendmsg.emit(msg)

    def clean_msg(self):
        """清理日志输出框"""
        self.ui.pte_msg.clear()

    def stop_run(self):
        self.stop = True

    def run(self):
        pass