# -*- coding: utf-8 -*-
import os
import random
import time
from PyQt5.QtCore import pyqtSignal

from src.conf.config import config
from src.func.base import Base, screenshot_dir

loop_fengmo = [
    'receive',
    'box',
    'fight',
    'end'
]

loop_douji = [
    'receive',
    'fight',
    'auto',
    'auto1',
    'mvp',
    'reward',
    'victory',
    'defeat',
]
loop_activity = [
    'receive',
    'fight',
    'reward',
    'victory',
]

class Robot(Base):
    # 定义类属性为信号函数
    sendmsg = pyqtSignal(str)  #msg

    def __init__(self, config):
        super(Robot, self).__init__()
        self.stop = True
        self.config = config
        self.type = config.robot['type']

    def loop(self):

        if self.type == "逢魔":
            stages_loop = loop_fengmo
            second_dir = 'robot/fengmo'
        elif self.type == "斗技":
            stages_loop = loop_douji
            second_dir = 'robot/douji'
        else :
            stages_loop = loop_activity
            second_dir = 'robot/activity'
        aim_num = int(config.general['times'])
        count = 0
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

            if found is False:
                time.sleep(0.3)  # 常规情况下，休眠1秒
                continue
            else:
                if key == 'fight':
                    time.sleep(random.uniform(0.5, 1))
                    self.tap(loc[0], loc[1])
                    time.sleep(0.5)
                    self.display_msg("开始第{0}次战斗，当前时间为:{1}".format(count + 1, self.get_time_stmps))
                    count += 1
                elif key == 'reward':
                    time.sleep(random.uniform(2, 3))
                    self.tapOther()
                elif key == 'victory':
                    time.sleep(random.uniform(0.3, 2))
                    self.tap(loc[0], loc[1])
                    self.display_msg("第{0}次战斗胜利，当前时间为:{1}".format(count, self.get_time_stmps))
                elif key == 'defeat':
                    time.sleep(random.uniform(0.3, 2))
                    self.tap(loc[0], loc[1])
                    self.display_msg("第{0}次战斗失败，当前时间为:{1}".format(count, self.get_time_stmps))
                elif key == 'receive':
                    time.sleep(random.uniform(0.3, 2))
                    self.tap(loc[0], loc[1])
                    self.display_msg("有新的协作已经接取，请注意查看！！")
                elif key == 'end':
                    self.stop = True
                    self.display_msg("自动化结束！")
                else:
                    time.sleep(random.uniform(0.3, 1))
                    self.tap(loc[0], loc[1])

            if count == aim_num:
                self.stop = True
                self.display_msg("战斗结束！")

            time.sleep(random.uniform(1, 2))


    def run(self):
        self.resize_win_size()
        self.loop()

if __name__ == '__main__':
    robot = Robot(config)
    robot.run()
