import sys
import socket               # 导入 socket 模块
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QThread
import pymysql

class NewThread(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        host = socket.gethostname()      # 获取本地主机名
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 创建 socket 对象
        self.s.bind((host, MainWindow.port))        # 绑定端口
        print('excute')
        self.s.listen(5)                      # 等待客户端连接
        self.c, addr = self.s.accept()        # 建立客户端连接。
        print ('连接地址：', addr)
        print('here')
        while(self.c.recv(1024)):
            self.t=self.c.recv(1024).decode("utf8")
            GUIthread=GUIchange()
            GUIthread.start()

class GUIchange(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        if(int(MainWindow.lightthread.t)==1):
            MainWindow.Lighton()
        else:
            MainWindow.Lightoff()

class Initwindow(QWidget):
    def __init__(self, left, up, width, height, title, icon):
        super().__init__()
        self.initUI(left, up, width, height, title, icon)

    def initUI(self, left, up, width, height,  title, icon):
        # 连接MySQL数据库
        connection = pymysql.connect("localhost","root","12345678","smarthome" )
       # 通过cursor创建游标
        cursor = connection.cursor()
       # 创建sql 语句，并执行
        sql = "SELECT `status` FROM `lightstatus1` WHERE `id`=1"
        cursor.execute(sql)
        result = cursor.fetchone()
        status = int(result[0])
       # 提交SQL
        connection.commit()
        connection.close()
        self.setWindowTitle(title)
        self.setGeometry(left, up, width, height)
        self.setWindowIcon(QIcon(icon))
        #添加布局
        self.MainLayout=QVBoxLayout()
        self.HLayout = QHBoxLayout()
        self.HLayout2=QHBoxLayout()
        #添加标签
        self.address=QLabel('请输入端口:(0-65535)')
        #添加图片
        self.lbl = QLabel(self)
        self.pixmap = QPixmap("lightoff.png")
        self.lbl.setPixmap(self.pixmap)
        # 添加编辑框（QLineEdit）
        self.lineEdit = QLineEdit("")
        #按钮
        self.btnconnect = QPushButton(u'匹配设备', parent=self)
        self.btndisconnect = QPushButton(u'断开连接', parent=self)
        self.btnlightoff = QPushButton(u'关闭', parent=self)
        self.btnlighton = QPushButton(u'打开', parent=self)
        # 放入布局内
        self.HLayout.addWidget(self.address)
        self.HLayout.addWidget(self.lineEdit)
        self.HLayout.addWidget(self.btnconnect)
        self.HLayout.addWidget(self.btndisconnect)
        self.HLayout2.addWidget(self.btnlighton)
        self.HLayout2.addWidget(self.btnlightoff)
        self.MainLayout.addLayout(self.HLayout)
        self.MainLayout.addLayout(self.HLayout2)
        self.MainLayout.addWidget(self.lbl)
        #连接槽
        self.btnconnect.clicked.connect(self.Connecttoserver)
        self.btndisconnect.clicked.connect(self.Disconnectfromserver)
        self.btnlighton.clicked.connect(self.Lighton)
        self.btnlightoff.clicked.connect(self.Lightoff)
        if status == 1:
            self.Lighton()
        if status == 0:
            self.Lightoff()
        self.setLayout(self.MainLayout)
        self.show()

    def Connecttoserver(self):
        PortNum = self.lineEdit.text()
        self.port = int(PortNum)
        if(self.port>=0&self.port<=65535):
             self.lineEdit.setEnabled(0)
             self.btndisconnect.setEnabled(1)
             self.btnconnect.setEnabled(0)
             self.lightthread=NewThread()
             self.lightthread.start()

    def Disconnectfromserver(self):
        self.lightthread.s.close()
        print("已断开")
        self.pixmap = QPixmap("lightoff.png")
        self.lbl.setPixmap(self.pixmap)
        self.MainLayout.addWidget(self.lbl)
        self.lineEdit.setEnabled(1)
        self.btndisconnect.setEnabled(0)
        self.btnconnect.setEnabled(1)

    def Lighton(self):
        self.pixmap = QPixmap("lighton.png")
        self.lbl.setPixmap(self.pixmap)
        connection = pymysql.connect("localhost","root","12345678","smarthome" )
        # 通过cursor创建游标
        cursor = connection.cursor()
        # 创建sql 语句，并执行
        sql = "UPDATE `lightstatus1` set `status`=1 where(`id`=1) "
        cursor.execute(sql)
        # 提交SQL
        connection.commit()

    def Lightoff(self):
        self.pixmap = QPixmap("lightoff.png")
        self.lbl.setPixmap(self.pixmap)
        connection = pymysql.connect("localhost","root","12345678","smarthome" )
        # 通过cursor创建游标
        cursor = connection.cursor()
        # 创建sql 语句，并执行
        sql = "UPDATE `lightstatus1` set `status`=0 where(`id`=1) "
        cursor.execute(sql)
        # 提交SQL
        connection.commit()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   MainWindow = Initwindow(200, 150, 450, 350, '电灯客户端', 'home.ico')
   sys.exit(app.exec_())


