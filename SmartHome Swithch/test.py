#encoding=utf-8
import sys
import socket               # 导入 socket 模块
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread,QSize, Qt
from functools import partial
import time
import pymysql
class Initwindow(QWidget):

    def __init__(self, left, up, width, height, title, icon):
        super().__init__()
        self.initUI(left, up, width, height, title, icon)

    def initUI(self, left, up, width, height,  title, icon):
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle(title)
        self.setGeometry(left, up, width, height)
        self.setWindowIcon(QIcon(icon))
        self.show()
if __name__ == '__main__':
   app = QApplication(sys.argv)
   MainWindow = Initwindow(200, 150, 500, 500, '智能家居开关', 'home.ico')
   sys.exit(app.exec_())
