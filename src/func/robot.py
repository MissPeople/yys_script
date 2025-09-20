# -*- coding: utf-8 -*-
import os
import random
import time
from PyQt5.QtCore import pyqtSignal

from src.func.base import Base, screenshot_dir

loop_fengmo = []
loop_shoulie = []
loop_douji = []
loop_activity = [
    'fight',
    'select_boss',
    'reward'
]

class Robot(Base):
    # 定义类属性为信号函数
    sendmsg = pyqtSignal(str)  #msg

    def __init__(self, config):
        super(Robot, self).__init__()
        self.stop = True
        self.config = config

    def loop(self):

        if self.config.robot['type'] == "逢魔":
            stages_loop = loop_fengmo
            second_dir = 'robot/fengmo'
        elif self.config.robot['type'] == "狩猎":
            stages_loop = loop_shoulie
            second_dir = 'robot/shoulie'
        elif self.config.robot['type'] == "斗技":
            stages_loop = loop_douji
            second_dir = 'robot/douji'
        else :
            stages_loop = loop_activity
            second_dir = 'robot/activity'

        count = 0
        self.stop = False
        while self.stop is False:
            found = False
            key = ''
            loc = None
            im_yys = self.screenshot()
            for key in stages_loop:
                img_path = os.path.join(screenshot_dir, second_dir, f"{key}.png")
                loc = self.find_img(img_path, im_yys)
                if loc is not None:
                    found = True
                    break

            if found is False:
                time.sleep(1)  # 常规情况下，休眠1秒
                continue
            else:
                if key == 'fight':
                    self.tap(loc[0], loc[1])
                    self.display_msg("开始第{0}次战斗".format(count + 1))
                    time.sleep(random.uniform(0.5, 1.5))
                elif key == 'select_boss':
                    time.sleep(random.uniform(0.3, 2))
                    self.tap(loc[0], loc[1])
                    time.sleep(170)
                else:
                    count += 1
                    time.sleep(random.uniform(0.3, 2))
                    self.tap(loc[0], loc[1])
                    time.sleep(random.uniform(2, 3))
            if count == 200:
                self.stop = True


    def run(self):
        self.resize_win_size()
        self.loop()
