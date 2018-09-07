#encoding=utf-8
import sys
import socket               # 导入 socket 模块
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread,QSize, Qt
from functools import partial
import time
import pymysql

#socket进程
class NewThread(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        PortNum = MainWindow.light.port1.text()
        self.port = int(PortNum)
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = socket.gethostname()
        self.s.connect((host, self.port))
        self.Statuschange = Afterconnect()
        self.Statuschange.start()

#连接后ui改变
class Afterconnect(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        MainWindow.light.btnon1.setEnabled(1)
        MainWindow.light.btnoff1.setEnabled(1)

#连接后ui改变
class ontimer(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        self.minute = MainWindow.light.minuteedit.text()
        self.second = MainWindow.light.secondedit.text()
        self.intminute = int(self.minute)
        self.intsecond = int(self.second)
        self.ontime = self.intminute*60 + self.intsecond
        print(self.ontime)
        time.sleep(self.ontime)
        if MainWindow.light.lightstatus == 1:
            MainWindow.light.lighton()
        MainWindow.light.startcount.setEnabled(1)
        MainWindow.light.endcount.setEnabled(1)
        MainWindow.light.minuteedit.setEnabled(1)
        MainWindow.light.secondedit.setEnabled(1)

class offtimer(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        self.minute = MainWindow.light.minuteedit.text()
        self.second = MainWindow.light.secondedit.text()
        self.intminute = int(self.minute)
        self.intsecond = int(self.second)
        self.offtime = self.intminute*60 + self.intsecond
        print(self.offtime)
        if MainWindow.light.lightstatus == 1:
            MainWindow.light.lightoff()
        time.sleep(self.offtime)
        MainWindow.light.startcount.setEnabled(1)
        MainWindow.light.endcount.setEnabled(1)
        MainWindow.light.minuteedit.setEnabled(1)
        MainWindow.light.secondedit.setEnabled(1)
#添加灯按钮的类
class addlight(QWidget):
    def __init__(self,name):
        super(addlight,self).__init__()
        self.Initlight(name)
    def Initlight(self,name):
        self.setWindowIcon(QIcon('home.ico'))
        self.setWindowFlags(Qt.SubWindow)
        self.resize(250, 200)
        self.move(250,200)
        self.Vlayout1 = QVBoxLayout()
        self.Vlayout2 = QVBoxLayout()
        self.Hlayout0 = QHBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.Hlayout3 = QHBoxLayout()
        self.Hlayout4 = QHBoxLayout()
        self.Hlayout5 = QHBoxLayout()
        #获取名称
        self.name = name
        self.connection2 = pymysql.connect("localhost","root","12345678","smarthome",charset='utf8' )
        self.cursor2 = self.connection2.cursor()
        sql = "SELECT status FROM `equipmentstatus` WHERE name='%s' "%(name)
        self.cursor2.execute(sql)
        self.connection2.commit()
        result = self.cursor2.fetchone()

        if int(result[0]) == 0:
            self.label0 = QLabel('设备已关闭')
        if int(result[0]) == 1:
            self.label0 = QLabel('设备已开启')
        #从数据库中获取端口
        sql = "SELECT port FROM `equipmentstatus` WHERE name='%s' "%(name)
        self.cursor2.execute(sql)
        self.connection2.commit()
        portnum= self.cursor2.fetchone()
        port = str(portnum[0])
        #组件初始化
        self.label1 = QLabel('请输入端口号')
        self.port1 = QLineEdit(port)
        self.btnconnect1= QPushButton(u'匹配设备', parent=self)
        self.btncancel1 = QPushButton(u'取消匹配', parent=self)
        self.btnon1 = QPushButton(u'打开', parent=self)
        self.btnoff1 = QPushButton(u'关闭', parent=self)
        self.btnon1.setEnabled(0)
        self.btnoff1.setEnabled(0)
        self.timelabel = QLabel('定时器')
        self.minutelabel = QLabel('分')
        self.secondlabel = QLabel('秒')
        self.minuteedit = QLineEdit('')
        self.secondedit = QLineEdit('')
        self.startcount = QPushButton('开灯计时')
        self.endcount = QPushButton('关灯计时')
        self.cancelcount = QPushButton('取消计时')
        self.Hlayout0.addWidget(self.label0)

        self.Hlayout1.addWidget(self.label1)
        self.Hlayout1.addWidget(self.port1)

        self.Hlayout2.addWidget(self.btnconnect1)
        self.Hlayout2.addWidget(self.btncancel1)

        self.Hlayout3.addWidget(self.btnon1)
        self.Hlayout3.addWidget(self.btnoff1)

        self.Hlayout4.addWidget(self.minuteedit)
        self.Hlayout4.addWidget(self.minutelabel)
        self.Hlayout4.addWidget(self.secondedit)
        self.Hlayout4.addWidget(self.secondlabel)




        self.Vlayout2.addWidget(self.timelabel)
        self.Vlayout2.addLayout(self.Hlayout4)

        self.Vlayout2.addWidget(self.startcount)
        self.Vlayout2.addWidget(self.endcount)
        self.Vlayout2.addWidget(self.cancelcount)

        self.Vlayout1.addLayout(self.Hlayout1)
        self.Vlayout1.addLayout(self.Hlayout2)
        self.Vlayout1.addLayout(self.Hlayout3)
        self.Vlayout1.addLayout(self.Vlayout2)
        self.Vlayout1.addLayout(self.Hlayout0)
        self.setLayout(self.Vlayout1)

        self.btnconnect1.clicked.connect(self.connecttoclient)
        self.btncancel1.clicked.connect(self.disconnect)
        self.btnon1.clicked.connect(self.lighton)
        self.btnoff1.clicked.connect(self.lightoff)
        self.startcount.clicked.connect(self.oncount)
        self.endcount.clicked.connect(self.offcount)
        self.cancelcount.clicked.connect(self.cancel)
        self.btncancel1.setEnabled(0)
    def cancel(self):
        self.lightstatus = 0
        MainWindow.light.startcount.setEnabled(1)
        MainWindow.light.endcount.setEnabled(1)
        MainWindow.light.minuteedit.setEnabled(1)
        MainWindow.light.secondedit.setEnabled(1)
    def oncount(self):
        self.lightstatus = 1
        self.time = ontimer()
        self.time.start()
        self.secondedit.setEnabled(0)
        self.minuteedit.setEnabled(0)
        self.startcount.setEnabled(0)
        self.endcount.setEnabled(0)
    def offcount(self):
        self.lightstatus = 1
        self.time = offtimer()
        self.time.start()
        self.secondedit.setEnabled(0)
        self.minuteedit.setEnabled(0)
        self.startcount.setEnabled(0)
        self.endcount.setEnabled(0)
    def connecttoclient(self):
        PortNum = self.port1.text()
        self.port = int(PortNum)
        if(self.port>=0&self.port<=65535):
            self.btnconnect1.setEnabled(0)
            self.btncancel1.setEnabled(1)
            self.port1.setEnabled(0)
            sql = "UPdate `equipmentstatus` SET port='%d' WHERE name='%s' "%(self.port,self.name)
            self.cursor2.execute(sql)
            self.connection2.commit()
            self.ListenThread = NewThread()
            self.ListenThread.start()

    def disconnect(self):
        self.btnconnect1.setEnabled(1)
        self.port1.setEnabled(1)
        self.btncancel1.setEnabled(0)
        self.btnon1.setEnabled(0)
        self.btnoff1.setEnabled(0)
        self.ListenThread.s.close()
    def lighton(self):

        sql = "UPdate `equipmentstatus` SET status=1 WHERE name='%s' "%(self.name)
        self.cursor2.execute(sql)
        self.connection2.commit()
        message='1'
        for i in reversed(range(self.Hlayout0.count())):
            widgetToRemove = self.Hlayout0.itemAt(i).widget()
            self.Hlayout0.removeWidget( widgetToRemove )
            widgetToRemove.setParent( None )
        self.label0 = QLabel('设备已开启')
        self.Hlayout0.addWidget(self.label0)
        self.Vlayout1.addLayout(self.Hlayout1)
        self.Vlayout1.addLayout(self.Hlayout2)
        self.Vlayout1.addLayout(self.Hlayout3)
        self.Vlayout1.addLayout(self.Vlayout2)
        self.Vlayout1.addLayout(self.Hlayout0)
        self.setLayout(self.Vlayout1)
        self.ListenThread.s.send (bytes(message,'utf-8'))
        self.ListenThread.s.send (bytes(message,'utf-8'))
    def lightoff(self):
        sql = "UPdate `equipmentstatus` SET status=0 WHERE name='%s' "%(self.name)
        self.cursor2.execute(sql)
        self.connection2.commit()
        message='0'
        for i in reversed(range(self.Hlayout0.count())):
            widgetToRemove = self.Hlayout0.itemAt(i).widget()
            # remove it from the layout list
            self.Hlayout0.removeWidget( widgetToRemove )
            # remove it from the gui
            widgetToRemove.setParent( None )
        self.label0 = QLabel('设备已关闭')
        self.Hlayout0.addWidget(self.label0)
        self.Vlayout1.addLayout(self.Hlayout1)
        self.Vlayout1.addLayout(self.Hlayout2)
        self.Vlayout1.addLayout(self.Hlayout3)
        self.Vlayout1.addLayout(self.Vlayout2)
        self.Vlayout1.addLayout(self.Hlayout0)
        self.setLayout(self.Vlayout1)
        self.ListenThread.s.send (bytes(message,'utf-8'))
        self.ListenThread.s.send (bytes(message,'utf-8'))
#添加按钮的窗口类
class AddWindow(QWidget):
    def __init__(self):
        super(AddWindow,self).__init__()
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
        self.rb23 = QRadioButton('电吹风',self)
        self.name = QLineEdit("")
        self.bg1 = QButtonGroup(self)
        self.bg1.addButton(self.rb11,1)
        self.bg1.addButton(self.rb12,2)
        self.bg1.addButton(self.rb13,3)
        self.bg1.addButton(self.rb21,4)
        self.bg1.addButton(self.rb22,5)
        self.bg1.addButton(self.rb23,6)
        self.namelabel = QLabel('请输入设备名字:')
        self.submit = QPushButton(u'添加设备',parent=self)
        self.submit.clicked.connect(self.addequipment)

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

    def addequipment(self):
        self.newname = self.name.text()
        self.connection1 = pymysql.connect("localhost","root","12345678","smarthome",charset='utf8' )
        self.cursor1 = self.connection1.cursor()
        if self.rb11.isChecked() == 1:
            try:
                sql = "INSERT INTO equipmentstatus(name, \
                      status, kind) \
                      VALUES ('%s', '%d', '%d' )" % \
                      (self.newname, 0,1)
                self.cursor1.execute(sql)
                self.connection1.commit()
                self.submit.setEnabled(0)
                self.close()
                MainWindow.sidebar()
            except:
                self.connection1.rollback()
        if self.rb12.isChecked() == 1:
            try:
                sql = "INSERT INTO equipmentstatus(name, \
                      status, kind) \
                      VALUES ('%s', '%d', '%d' )" % \
                      (self.newname, 0,2)
                self.cursor1.execute(sql)
                self.connection1.commit()
                self.submit.setEnabled(0)
                self.close()
                MainWindow.sidebar()
            except:
                self.connection1.rollback()
        if self.rb13.isChecked() == 1:
            try:
                sql = "INSERT INTO equipmentstatus(name, \
                      status, kind) \
                      VALUES ('%s', '%d', '%d' )" % \
                      (self.newname, 0,3)
                self.cursor1.execute(sql)
                self.connection1.commit()
                self.submit.setEnabled(0)
                self.close()
                MainWindow.sidebar()
            except:
                self.connection1.rollback()
        if self.rb21.isChecked() == 1:
            try:
                sql = "INSERT INTO equipmentstatus(name, \
                      status, kind) \
                      VALUES ('%s', '%d', '%d' )" % \
                      (self.newname, 0,4)
                self.cursor1.execute(sql)
                self.connection1.commit()
                self.submit.setEnabled(0)
                self.close()
                MainWindow.sidebar()
            except:
                self.connection1.rollback()
        if self.rb22.isChecked() == 1:
            try:
                sql = "INSERT INTO equipmentstatus(name, \
                      status, kind) \
                      VALUES ('%s', '%d', '%d' )" % \
                      (self.newname, 0,5)
                self.cursor1.execute(sql)
                self.connection1.commit()
                self.submit.setEnabled(0)
                self.close()
                MainWindow.sidebar()
            except:
                self.connection1.rollback()
        if self.rb23.isChecked() == 1:
            try:
                sql = "INSERT INTO equipmentstatus(name, \
                      status, kind) \
                      VALUES ('%s', '%d', '%d' )" % \
                      (self.newname, 0,6)
                self.cursor1.execute(sql)
                self.connection1.commit()
                self.submit.setEnabled(0)
                self.close()
                MainWindow.sidebar()
            except:
                self.connection1.rollback()
#删除按钮的窗口类
class Deletewindow(QWidget):
    def __init__(self):
        super(Deletewindow,self).__init__()
        self.setWindowIcon(QIcon('home.ico'))
        self.setWindowFlags(Qt.Tool)
        self.resize(250, 200)
        self.move(250,200)
        self.deletelayout = QVBoxLayout()
        self.deletetip = QLabel('请输入需要删除设备的名字：')
        self.deletename = QLineEdit('')
        self.deletebutton = QPushButton(u'删除设备',parent=self)
        self.deletelayout.addWidget(self.deletetip)
        self.deletelayout.addWidget(self.deletename)
        self.deletelayout.addWidget(self.deletebutton)
        self.setLayout(self.deletelayout)
        self.deletebutton.clicked.connect(self.fucdelete)
    def fucdelete(self):
        self.connection1= pymysql.connect("localhost","root","12345678","smarthome",charset='utf8' )
        self.cursor1 = self.connection1.cursor()

        try:
            sql = "DELETE FROM equipmentstatus\
                   WHERE name = ('%s' )" % \
                   (self.deletename.text())
            self.cursor1.execute(sql)
            self.connection1.commit()
            self.close()
            MainWindow.sidebar()
        except:
            self.connection1.rollback()
#主窗口类
class Initwindow(QWidget):

    def __init__(self, left, up, width, height, title, icon):
        super().__init__()
        self.initUI(left, up, width, height, title, icon)

    def initUI(self, left, up, width, height,  title, icon):
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle(title)
        self.setGeometry(left, up, width, height)
        self.setWindowIcon(QIcon(icon))
        #布局初始化
        self.Vlayout = QVBoxLayout()
        self.sidelayoutup = QVBoxLayout()
        self.sidelayoutdown = QVBoxLayout()
        self.Mainlayout = QHBoxLayout()
         #添加设备
        self.sidebtnadd = QPushButton(u'添加设备', parent=self)
        self.sidebtnadd.setIcon(QIcon('addico.png'))
        self.sidebtnadd.setIconSize(QSize(50,50))
        self.sidebtnadd.resize(QSize(50,50))
        self.sidelayoutup.addWidget(self.sidebtnadd)
        #删除设备
        self.sidebtndelete = QPushButton(u'删除设备', parent=self)
        self.sidebtndelete.setIcon(QIcon('deleteico.png'))
        self.sidebtndelete.setIconSize(QSize(50,50))
        self.sidebtndelete.resize(QSize(50,50))
        self.sidelayoutup.addWidget(self.sidebtndelete)
        self.sidebar()
        self.setLayout(self.Mainlayout)
        #添加响应
        self.sidebtnadd.clicked.connect(self.addnewwidget)
        self.sidebtndelete.clicked.connect(self.deletewidget)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.connection.commit()
        self.connection.close()
        self.show()

    def sidebar(self):
        # 连接MySQL数据库
        for i in reversed(range(self.sidelayoutdown.count())):
            widgetToRemove = self.sidelayoutdown.itemAt(i).widget()
            # remove it from the layout list
            self.sidelayoutdown.removeWidget( widgetToRemove )
            # remove it from the gui
            widgetToRemove.setParent( None )
        self.connection = pymysql.connect("localhost","root","12345678","smarthome",charset='utf8' )
        self.cursor = self.connection.cursor()
        sql = "SELECT max(id) FROM `equipmentstatus` "
        self.cursor.execute(sql)
        self.number = self.cursor.fetchone()
        sql = "SELECT * FROM `equipmentstatus` "
        self.cursor.execute(sql)
        self.button={}
        for self.buttonnumber in range(0, int(self.number[0])):
            result = self.cursor.fetchone()
            if result == None:break
            self.button[self.buttonnumber] = QPushButton(result[2])
            #电灯
            if result[3] == 1:
                self.button[self.buttonnumber].setIcon(QIcon('lightico.png'))
                self.button[self.buttonnumber].setIconSize(QSize(50,50))
                self.button[self.buttonnumber].resize(QSize(50,50))
                self.sidelayoutdown.addWidget(self.button[self.buttonnumber])
                self.button[self.buttonnumber].clicked.connect(partial(self.lightwidget, self.buttonnumber,result[2]))
            #空调
            if result[3] == 2:
                self.button[self.buttonnumber].setIcon(QIcon('airico.png'))
                self.button[self.buttonnumber].setIconSize(QSize(50,50))
                self.button[self.buttonnumber].resize(QSize(50,50))
                self.sidelayoutdown.addWidget(self.button[self.buttonnumber])
                #self.button[i].clicked.connect(self.airwidget)
            #洗衣机
            if result[3] == 3:
                self.button[self.buttonnumber].setIcon(QIcon('washico.png'))
                self.button[self.buttonnumber].setIconSize(QSize(50,50))
                self.button[self.buttonnumber].resize(QSize(50,50))
                self.sidelayoutdown.addWidget(self.button[self.buttonnumber])
            if result[3] == 4:
                self.button[self.buttonnumber].setIcon(QIcon('lockico.png'))
                self.button[self.buttonnumber].setIconSize(QSize(50,50))
                self.button[self.buttonnumber].resize(QSize(50,50))
                self.sidelayoutdown.addWidget(self.button[self.buttonnumber])
            if result[3] == 5:
                self.button[self.buttonnumber].setIcon(QIcon('waterico.png'))
                self.button[self.buttonnumber].setIconSize(QSize(50,50))
                self.button[self.buttonnumber].resize(QSize(50,50))
                self.sidelayoutdown.addWidget(self.button[self.buttonnumber])
            if result[3] == 6:
                self.button[self.buttonnumber].setIcon(QIcon('dryerico.png'))
                self.button[self.buttonnumber].setIconSize(QSize(50,50))
                self.button[self.buttonnumber].resize(QSize(50,50))
                self.sidelayoutdown.addWidget(self.button[self.buttonnumber])
        # 放入布局内
        self.sidelayoutup.addLayout(self.sidelayoutdown)
        self.Mainlayout.addLayout(self.sidelayoutup)
        self.Mainlayout.addLayout(self.Vlayout)

    def addnewwidget(self):
        self.child=AddWindow()         #添加子窗口
        self.child.show()

    def deletewidget(self):
        self.child=Deletewindow()
        self.child.show()

    def lightwidget(self,count,name):
        #清空layout
        for i in reversed(range(self.Vlayout.count())):
            widgetToRemove = self.Vlayout.itemAt(i).widget()
            # remove it from the layout list
            self.Vlayout.removeWidget( widgetToRemove )
            # remove it from the gui
            widgetToRemove.setParent( None )
        self.light = addlight(name)
        self.Vlayout.addWidget(self.light)
        self.Mainlayout.addLayout(self.Vlayout)
        for i in reversed(range(self.sidelayoutdown.count())):
            self.widgetTobeable = self.sidelayoutdown.itemAt(i).widget()
            self.widgetTobeable.setEnabled(1)
        self.button[count].setEnabled(0)
if __name__ == '__main__':
   app = QApplication(sys.argv)
   MainWindow = Initwindow(200, 150, 500, 500, '智能家居开关', 'home.ico')
   sys.exit(app.exec_())

