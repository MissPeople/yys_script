# -*- coding: utf-8 -*-
import os
import random
import time
from PyQt5.QtCore import pyqtSignal

from src.func.base import Base, screenshot_dir
from src.conf import config

loop_douji = [
    'receive',
    'reward',
    'fight_douji',
    'auto',
    'auto1',
    'mvp',
    'victory',
    'defeat',
]

loop_juexin_yulin = [
    'receive',
    'fight_food_6',
    'fight_yulin',
    'reward',
    'victory',
]

loop_activity = [
    'receive',
    'fight_activity',
    'reward'
]

class Robot(Base):
    # 定义类属性为信号函数
    sendmsg = pyqtSignal(str)  #msg

    def __init__(self):
        super(Robot, self).__init__()
        self.stop = True
        self.type = config.robot['type']

    def loop(self):

        if self.type == "斗技":
            stages_loop = loop_douji
            execute_dir = 'robot/douji'
        elif self.type == "觉醒/御灵":
            stages_loop = loop_juexin_yulin
            execute_dir = 'robot/juexin_yulin'
        else :
            stages_loop = loop_activity
            execute_dir = 'robot/activity'

        aim_count = int(config.general['times'])
        executed_count = 0
        
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
                    img_path = os.path.join(screenshot_dir, execute_dir, f"{key}.png")
                loc = self.find_img(img_path, im_yys)
                if loc is not None:
                    found = True
                    break

            if found is False:
                time.sleep(0.5)  # 常规情况下，休眠0.5秒,再执行扫描
                continue
            else:
                if key in ['fight_douji', 'fight_food_6', 'fight_yulin', 'fight_activity']:
                    time.sleep(random.uniform(0.5, 1))
                    self.tap(loc[0], loc[1])
                    self.display_msg("开始第{0}次战斗，当前时间为:{1}".format(executed_count + 1, self.get_time_stmps()))
                    executed_count += 1
                elif key == 'reward':
                    time.sleep(random.uniform(2, 3))
                    self.tapOther()
                    time.sleep(random.uniform(0.5, 2))
                elif key == 'victory':
                    time.sleep(random.uniform(0.3, 2))
                    self.tapOther()
                elif key == 'receive':
                    time.sleep(random.uniform(0.3, 2))
                    self.tap(loc[0], loc[1])
                    self.display_msg("有新的协作已经接取，请注意查看！！,接收时间为:{0}".format(self.get_time_stmps()))
                else:
                    time.sleep(random.uniform(0.3, 2))
                    self.tap(loc[0], loc[1])

            if executed_count == aim_count:
                self.stop = True
                self.display_msg("战斗结束！")

            time.sleep(random.uniform(1, 2))


    def run(self):
        self.display_msg(f"欢迎使用阴阳师自动化脚本!\n当前设备:{config.general['win_name']}\n当前端口:{config.general['adb_port']}\n当前功能:机器人-{self.type}\n当前设置战斗次数:{config.general['times']}\n开始运行，请稍后...")
        self.resize_win_size()
        self.loop()
        self.display_msg("挂机结束，回到初始界面！")