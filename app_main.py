# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal

from src.func.robot import Robot
from src.ui import main_widget as UI
from src.conf import config
from src.func import *

def set_ui_cmbox(cb, lines):
    '''给一个具体的combox控件添加显示项目'''
    cb.clear()
    cb.addItems(lines)


class YysWin(QMainWindow):
    stop_run = pyqtSignal()

    def __init__(self):
        super(YysWin, self).__init__()
        self.ui = UI.Ui_yys_win()
        self.ui.setupUi(self)
        self.init_win()

    def init_win(self):
        self.ui.pte_msg.clear()
        self.has_start = False
        self.type = ''

        # 绑定信号和槽
        self.ui.pbt_autocheck.clicked.connect(self.btn_autocheck_clicked)

        # 功能选项
        yys_funcs = ["御魂", "困28", "结界突破", '机器人']
        set_ui_cmbox(self.ui.cb_fuctions, yys_funcs)

    def display_msg(self, msg):
        """输出日志到框内"""
        self.ui.pte_msg.moveCursor(QtGui.QTextCursor.End)
        self.ui.pte_msg.insertPlainText(msg + '\n')

    def clean_msg(self):
        self.ui.pte_msg.clear()

    def set_comboxes(self, titles: list):
        '''通过列表来设置参数'''
        comboxes = [self.ui.cb_p1, self.ui.cb_p2, self.ui.cb_p3,self.ui.cb_p4]
        titles_len = len(titles)
        for i in range(4):
            if i < titles_len:
                set_ui_cmbox(comboxes[i], titles[i])
            else:
                set_ui_cmbox(comboxes[i], ['参数{}'.format(i + 1)])

    def cb_functions_index_changed(self):
        self.select_fun = self.ui.cb_fuctions.currentText()
        titles = []
        attentions = ''
        if self.select_fun == '御魂':
            attentions = config.yuhun['attention']
            titles = [['单人', '组队'], ['队长', '队员'], ['挂机次数', '30', '50', '120', '999'], ['魂土', '魂王']]
        elif self.select_fun == '困28':
            attentions = config.chapter['attention']
            titles = [['单人', '双人'], ['队长', '队员'],
                      ['挂机次数', '100', '200', '400', '9999'],
                      ['谁带输出', '队长', '队员'], ['狗粮类型', 'N卡', '白蛋']]
        elif self.select_fun == '结界突破':
            attentions = config.yys_break['attention']
            titles = []
        elif self.select_fun == '机器人':
            attentions = config.robot['attention']
            titles = [['副本', '逢魔', '狩猎', '斗技', '活动'],
                      ['挂机次数', '30', '50', '120', '999'],]

        self.show_attention(attentions)
        self.set_comboxes(titles)

    def get_config_from_param_cb(self):
        self.select_fun = self.ui.cb_fuctions.currentText()
        adb_port = self.ui.adb_port.text()
        config.general['win_name'] = self.ui.window_name.text()
        p1 = self.ui.cb_p1.currentText()
        p2 = self.ui.cb_p2.currentText()
        p3 = self.ui.cb_p3.currentText()
        p4 = self.ui.cb_p4.currentText()
        config.general['adb_port'] = adb_port if adb_port!='' else '5555'
        if self.select_fun == '御魂':
            config.yuhun['players'] = 1 if p1 == '单人' else 2
            config.yuhun['captain'] = p2 == '队长'
            # 这里防止未进行选择
            config.yuhun['times'] = 999
            if p3 == '30':
                config.yuhun['times'] = 3
            elif p3 == '50':
                config.yuhun['times'] = 50
            elif p3 == '120':
                config.yuhun['times'] = 120
            config.yuhun['select_tier'] = 'hun11'
            if p4 == '魂土':
                config.yuhun['select_tier'] = 'hun11'
            elif p4 == '魂王':
                config.yuhun['select_tier'] = 'hun12'
        elif self.select_fun == '机器人':
            config.robot['type'] = p1
            self.type = p1
            config.general['times'] = 0
            if p2 == '30':
                config.general['times'] = 30
            elif p2 == '50':
                config.general['times'] = 50
            elif p2 == '120':
                config.general['times'] = 120
            elif p2 == '999':
                config.general['times'] = 999

    def btn_autocheck_clicked(self):
        self.display_msg('自动挂机检测：{0}'.format(
            self.ui.cb_fuctions.currentText()))
        self.stop_run.emit()

    def btn_restart_clicked(self):
        self.btn_stop_clicked()
        self.btn_start_clicked()

    def btn_stop_clicked(self):
        self.display_msg('停止挂机：{0}'.format(self.select_fun))
        self.has_start = False
        self.stop_run.emit()
        self.show_attention(config.general['attention'] + '\n' + config.general['version'])

    def btn_start_clicked(self):
        # 从参数列表中选择参数
        self.get_config_from_param_cb()
        if self.has_start is True:
            self.display_msg('挂机已启动，请务重新启动，{0}' + self.select_fun)
            return

        self.display_msg('启动挂机：{0}:{1}'.format(self.select_fun, self.type))
        if self.select_fun == '御魂':
            self.display_msg('功能正在开发中。。。')
            # self.yuhun = yuhun1.Yuhun(yys_window, config.yuhun)
            # self.yuhun.sendmsg.connect(self.display_msg)
            # self.stop_run.connect(self.yuhun.stop_run)
            # self.has_start = True
            # self.yuhun.start()
        elif self.select_fun == '困28':
            self.display_msg('功能正在开发中。。。')
            # self.is_captain = config.chapter.get('captain', True)
            # if self.is_captain:
            #     self.chapter = chapter_captain.ChapterCaptain(self, config.chapter)
            # else:
            #     self.chapter = chapter.Chapter(self, config.chapter)
            # self.chapter.sendmsg.connect(self.display_msg)
            # self.stop_run.connect(self.chapter.stop_run)
            # self.has_start = True
            # self.chapter.start()
        elif self.select_fun == '机器人':
            self.robot = Robot(config)
            self.robot.sendmsg.connect(self.display_msg)
            self.stop_run.connect(self.robot.stop_run)
            self.has_start = True
            self.robot.start()

    def show_attention(self, content):
        self.ui.te_attention.setText(content)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = YysWin()
    main_win.show()
    sys.exit(app.exec_())