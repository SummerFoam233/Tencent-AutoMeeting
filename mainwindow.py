# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(343, 445)
        MainWindow.setMinimumSize(QtCore.QSize(250, 250))
        MainWindow.setMaximumSize(QtCore.QSize(400, 450))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(200, 200))
        self.frame.setMaximumSize(QtCore.QSize(270, 450))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(250, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
"background-color: rgb(81,81,81);\n"
"border-top-left-radius:8px;\n"
"border-top-right-radius:8px;\n"
"border-bottom-left-radius:8px;\n"
"border-bottom-right-radius:8px;\n"
"color:white;\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setStyleSheet("font-family:\"微软雅黑\"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.IDComBox = QtWidgets.QComboBox(self.frame_2)
        self.IDComBox.setEditable(True)
        self.IDComBox.setObjectName("IDComBox")
        self.gridLayout.addWidget(self.IDComBox, 0, 1, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 1)
        self.NameComBox = QtWidgets.QComboBox(self.frame_2)
        self.NameComBox.setEditable(True)
        self.NameComBox.setObjectName("NameComBox")
        self.gridLayout.addWidget(self.NameComBox, 1, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.StartTimeLE = QtWidgets.QLineEdit(self.frame_2)
        self.StartTimeLE.setObjectName("StartTimeLE")
        self.gridLayout.addWidget(self.StartTimeLE, 2, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        self.PasswdComBox = QtWidgets.QComboBox(self.frame_2)
        self.PasswdComBox.setEditable(True)
        self.PasswdComBox.setObjectName("PasswdComBox")
        self.gridLayout.addWidget(self.PasswdComBox, 3, 2, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)
        self.tmp_auto_course_pbt = QtWidgets.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tmp_auto_course_pbt.setFont(font)
        self.tmp_auto_course_pbt.setStyleSheet("QPushButton\n"
"{\n"
"    /*字体大小为14点*/\n"
"    font-size:12pt;\n"
"    /*字体颜色为白色*/    \n"
"    color:white;\n"
"    /*背景颜色*/  \n"
"    background-color:#878787;\n"
"    /*边框圆角半径为8像素*/ \n"
"    border-radius:7px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    /*背景颜色*/  \n"
"    background-color:#909090;\n"
"}\n"
"\n"
"/*按钮按下态*/\n"
"QPushButton:pressed\n"
"{\n"
"    /*背景颜色*/  \n"
"    background-color:#959595;\n"
"    /*左内边距为3像素，让按下时字向右移动3像素*/  \n"
"    padding-left:3px;\n"
"    /*上内边距为3像素，让按下时字向下移动3像素*/  \n"
"    padding-top:3px;\n"
"}\n"
"")
        self.tmp_auto_course_pbt.setObjectName("tmp_auto_course_pbt")
        self.gridLayout_2.addWidget(self.tmp_auto_course_pbt, 2, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoMeeting"))
        self.label.setText(_translate("MainWindow", "加入会议预定"))
        self.label_2.setText(_translate("MainWindow", "会议号："))
        self.label_9.setText(_translate("MainWindow", "姓名:"))
        self.label_3.setText(_translate("MainWindow", "开始时间:"))
        self.StartTimeLE.setPlaceholderText(_translate("MainWindow", "YYYY/MM/DD/hh-mm"))
        self.label_4.setText(_translate("MainWindow", "会议密码(可选):"))
        self.tmp_auto_course_pbt.setText(_translate("MainWindow", "开始托管"))
