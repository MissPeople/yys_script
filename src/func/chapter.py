# -*- coding: utf-8 -*-
import math
import os
import random
import time

import cv2
import numpy as np
from PIL import Image
from PyQt5.QtCore import pyqtSignal

from src.conf.config import config
from src.func.base import Base, screenshot_dir

stages_loop = [
    'receive',
    'treasure',
    'fight',
    'fight_boss',
    'reward',
    'tool',
    'victory',
    'search',
    'kun28',
    'box',
]

fight_path = os.path.join(screenshot_dir, 'chapter', 'fight.png')
fight_img = Image.open(fight_path)


class Chapter(Base):
    # 定义类属性为信号函数
    sendmsg = pyqtSignal(str)  #msg

    def __init__(self):
        super(Chapter, self).__init__()
        self.stop = True

    def loop(self):
        second_dir = 'chapter'
        aim_num = int(config.general['times'])
        count = 0
        not_found_count = 0
        self.stop = False
        while self.stop is False:
            found = False
            key = ''
            loc = None
            im_yys = self.screenshot()
            for key in stages_loop:
                if key == 'receive':
                    img_path = os.path.join(screenshot_dir, 'common', 'receive.png')
                else:
                    img_path = os.path.join(screenshot_dir, second_dir, f"{key}.png")
                loc = self.find_img(img_path, im_yys)

                if loc is not None:
                    found = True
                    break

            if found: 
                if key == 'fight':
                    time.sleep(random.uniform(0.5, 1))
                    self.tap(loc[0], loc[1])
                    count += 1
                elif key == 'reward':
                    time.sleep(random.uniform(2, 3))
                    self.tapOther()
                elif key == 'receive':
                    self.tap(loc[0], loc[1])
                    self.display_msg("有新的协作已经接取，请注意查看！！")
                else:
                    time.sleep(random.uniform(0.3, 2))
                    self.tap(loc[0], loc[1])
                not_found_count = 0
            else:
                not_found_count+=1

            if not_found_count == 3:
                self.tap(1580, 700)
                not_found_count = 0

            if count == aim_num:
                self.stop = True
                self.display_msg("战斗结束！")

            time.sleep(random.uniform(1, 2))


    def run(self):
        self.resize_win_size()
        self.loop()

if __name__ == '__main__':
    chapter = Chapter()
    chapter.run()
