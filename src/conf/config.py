#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% 加载基础库
import configparser
from src.tools.tool import get_resource_path

conf_path = get_resource_path('src/conf/config.ini')

class Config:
    def __init__(self):
        self.config = configparser.RawConfigParser()
        self.config.read(conf_path, encoding='utf-8')
        self.general = {}
        self.yuhun = {}
        self.chapter = {}
        self.yys_break = {}
        self.robot = {}
        self.init_config()

    def read_option_str(self, section, option, default):
        try:
            return self.config.get(section, option)
        except Exception as error:
            print('获取{0},{1}失败, {2}'.format(section, option, str(error)))
            return default

    def read_option_int(self, section, option, default):
        try:
            return self.config.getint(section, option)
        except Exception as error:
            print('获取{0},{1}失败, {2}'.format(section, option, str(error)))
            return default

    def read_option_bool(self, section, option, default):
        try:
            return self.config.getboolean(section, option)
        except Exception as error:
            print('获取{0},{1}失败, {2}'.format(section, option, str(error)))
            return default

    def init_config(self):
        self.general['title'] = self.read_option_str('general', 'title','YYS助手')
        self.general['version'] = self.read_option_str('general', 'version',  'v1.0.0')
        self.general['adb_port'] = self.read_option_str('general', 'adb_port', '5555')
        self.general['win_name'] = self.read_option_str('general', 'win_name', 'ios账号')
        self.general['times'] = self.read_option_int('general', 'times', 30)
        self.general['attention'] = self.read_option_str( 'general', 'attention', '').replace(r'\n', '\n')

        self.yuhun['type'] = self.read_option_str('yuhun', 'type', '魂十一')
        self.yuhun['players'] = self.read_option_int('yuhun', 'players', 2)
        self.yuhun['captain'] = self.read_option_bool('yuhun', 'captain', True)
        self.yuhun['attention'] = self.read_option_str('yuhun', 'attention','').replace(r'\n', '\n')

        self.chapter['players'] = self.read_option_int('chapter', 'players', 1)
        self.chapter['attention'] = self.read_option_str('chapter', 'attention', '').replace(r'\n', '\n')

        self.yys_break['attention'] = self.read_option_str('yys_break', 'attention', '').replace(r'\n', '\n')

        self.robot['type'] = self.read_option_str('robot', 'type', '逢魔')
        self.robot['attention'] = self.read_option_str('robot', 'attention', '').replace(r'\n', '\n')


config = Config()
general = config.general
yuhun = config.yuhun
yys_break = config.yys_break
chapter = config.chapter
robot = config.robot
