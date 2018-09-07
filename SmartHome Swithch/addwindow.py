import sys
import socket               # 导入 socket 模块
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread,QSize, Qt
class AddWindow(QWidget):
    def __init__(self):
        super(AddWindow,self).__init__()
        #self.setStyleSheet("background: black")
        self.setWindowIcon(QIcon('home.ico'))
        self.setWindowFlags(Qt.Tool)
        self.resize(250, 200)
        self.move(250,200)
        self.secondlayout = QVBoxLayout()
        self.gridlayout = QGridLayout()
        self.equipmentlabel = QLabel('请选择设备类型：')
        self.secondlayout.addWidget(self.equipmentlabel)
        self.secondlayout.addLayout(self.gridlayout)

        self.rb11 = QRadioButton('电灯',self)
        self.rb12 = QRadioButton('空调',self)
        self.rb13 = QRadioButton('洗衣机',self)
        self.rb21 = QRadioButton('门锁',self)
        self.rb22 = QRadioButton('热水壶',self)
        self.rb23 = QRadioButton('风扇',self)
        self.name = QLineEdit("")
        self.namelabel = QLabel('请输入设备名字:')
        self.submit = QPushButton(u'添加设备',parent=self)

        self.gridlayout.addWidget(self.rb11,0,0)
        self.gridlayout.addWidget(self.rb12,0,1)
        self.gridlayout.addWidget(self.rb13,2,0)
        self.gridlayout.addWidget(self.rb21,2,1)
        self.gridlayout.addWidget(self.rb22,4,0)
        self.gridlayout.addWidget(self.rb23,4,1)
        self.secondlayout.addLayout(self.gridlayout)
        self.secondlayout.addWidget(self.namelabel)
        self.secondlayout.addWidget(self.name)
        self.secondlayout.addWidget(self.submit)
        self.setLayout(self.secondlayout)
