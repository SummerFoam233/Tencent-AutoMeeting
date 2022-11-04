from PyQt5 import QtCore, QtGui, QtWidgets,QtMultimedia,QtMultimediaWidgets
from mainwindow import Ui_MainWindow
from PyQt5.QtCore import *
import time
from selenium import webdriver
import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import re
import winreg
import zipfile
import requests

class MainProgram(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainProgram,self).__init__(
            parent)
        self.setupUi(self)
        self.ClickEvent()
        self.StartTimeLE.setText(datetime.now().strftime("%Y/%m/%d/%H:%M"))
        self.base_url = 'http://npm.taobao.org/mirrors/chromedriver/'
        self.version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本号的正则表达式
        self.checkChromeDriverUpdate()
        
    def getChromeVersion(self):
        """通过注册表查询chrome版本"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Google\\Chrome\\BLBeacon')
            value, t = winreg.QueryValueEx(key, 'version')
            return self.version_re.findall(value)[0]  # 返回前3位版本号
        except WindowsError as e:
            self.QtMessageBox("critical","错误","未安装chrome浏览器，请安装后重试!")
            # 没有安装chrome浏览器
            return "1.1.1"
        
    def getChromeDriverVersion(self):
        """查询Chromedriver版本"""
        outstd2 = os.popen('chromedriver --version').read()
        try:
            version = outstd2.split(' ')[1]
            version = ".".join(version.split(".")[:-1])
            return version
        except Exception as e:
            return "0.0.0"


    def getLatestChromeDriver(self,version):
        # 获取该chrome版本的最新driver版本号
        url = f"{self.base_url}LATEST_RELEASE_{version}"
        latest_version = requests.get(url).text
        # print(f"与当前chrome匹配的最新chromedriver版本为: {latest_version}")
        # self.QtMessageBox("information","提示",f"与当前chrome匹配的最新chromedriver版本为: {latest_version}。\n开始下载...")

        download_url = f"{self.base_url}{latest_version}/chromedriver_win32.zip"
        file = requests.get(download_url)
        with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
            zip_file.write(file.content)
        # self.QtMessageBox("information","提示","下载完成,解压中...")
        # 解压
        f = zipfile.ZipFile("chromedriver.zip", 'r')
        for file in f.namelist():
            f.extract(file)

        # self.QtMessageBox("information","提示","解压完成!")


    def checkChromeDriverUpdate(self):
        chrome_version = self.getChromeVersion()
        driver_version = self.getChromeDriverVersion()
        if chrome_version == driver_version:
            #self.QtMessageBox("information","提示",f"当前chrome版本: {chrome_version}\n当前chromedriver版本: {driver_version}\n版本兼容，无需更新!")
            return
        # self.QtMessageBox("warning","警告","chromedriver版本与chrome浏览器不兼容，更新中>>>")
        try:
            self.getLatestChromeDriver(chrome_version)
            self.QtMessageBox("information","提示","chromedriver更新成功!")
            os.remove("chromedriver.zip")
        except requests.exceptions.Timeout:
            self.QtMessageBox("critical","错误","chromedriver下载失败，请检查网络后重试！")
        except Exception as e:
            self.QtMessageBox("critical","错误",f"chromedriver未知原因更新失败: {e}")
            
    def ClickEvent(self):
        self.tmp_auto_course_pbt.clicked.connect(self.auto_course_tmp_event)

    def verify_datetime(self,datetime_str):         
        # 比较日期格式是否正确
        try:
            datetime.strptime(datetime_str, '%Y/%m/%d/%H:%M')
        except ValueError:
            return False
        return True

    def auto_course_tmp_event(self):
        meeting_ID = self.MetIDLE.text()
        meeting_Name = self.NameLE.text()
        meeting_StartTime = self.StartTimeLE.text()
        
        if len(meeting_ID)==0:
            self.QtMessageBox("critical","错误","会议号不能为空!")
            return None
        if len(meeting_Name)==0:
            self.QtMessageBox("critical","错误","姓名不能为空!")
            return None
        if len(meeting_StartTime)==0:
            self.QtMessageBox("critical","错误","开始时间不能为空!")
            return None
        if self.verify_datetime(meeting_StartTime)==False:
            self.QtMessageBox("critical","错误","输入日期格式不合法，请重新检查!")
            return None
        curr_time = datetime.now().strftime("%Y/%m/%d/%H:%M")
        delta = (datetime.strptime(curr_time,"%Y/%m/%d/%H:%M") - datetime.strptime(meeting_StartTime,"%Y/%m/%d/%H:%M")).total_seconds()
        meet_time = datetime.strptime(meeting_StartTime,"%Y/%m/%d/%H:%M")
        if delta<0:
            self.QtMessageBox("information","预约成功","将在指定时间进入会议,请勿关闭电脑!")
        
            ontime_flag = False
        elif delta>=0:
            self.QtMessageBox("information","时间到","任务开始!")
            ontime_flag = True
            
        self.webthread = WebThread(meeting_ID,meeting_Name,ontime_flag,meet_time)
        self.webthread.start()
        
    def QtMessageBox(self,state,str_1,str_2):
        if state.lower() == 'information':
            self.Messagebox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,str_1,str_2)
        elif state.lower() == 'warning':
            self.Messagebox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,str_1,str_2)
        elif state.lower() == 'critical':
            self.Messagebox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,str_1,str_2)
        self.Messagebox.setWindowIcon(QtGui.QIcon('icons/logo.png'))
        self.Messagebox.show()
        return None
        
class WebThread(QtCore.QThread):
    finish = pyqtSignal(str)
    def __init__(self,meeting_ID,meeting_Name,ontime_flag,meet_time):
        super().__init__()
        self.meeting_ID = meeting_ID
        self.meeting_Name = meeting_Name
        self.ontime_flag = ontime_flag
        self.meet_time = meet_time
        self.sched = BlockingScheduler()
        
    def run_job(self,text):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")  # 隐身模式打开
            driver_path = r"chromedriver.exe"
            browser = webdriver.Chrome(driver_path, options=options)
            browser.get("https://voovmeeting.com/r")
            time.sleep(3)
            browser.find_elements_by_class_name("join-form__input")[0].send_keys(self.meeting_ID)
            browser.find_elements_by_class_name("join-form__input")[1].send_keys(self.meeting_Name)
            browser.find_element_by_css_selector(".tea-btn").click()
            time.sleep(3)
            browser.switch_to.frame(0)
            browser.find_element_by_css_selector(".met-btn").click()
            browser.find_element_by_css_selector(".met-checkbox").click()
            browser.find_element_by_css_selector(".met-btn").click()
        except:
            pass
        
    def run(self):
        if self.ontime_flag:
            self.run_job(None)
        else:
            self.sched.add_job(self.run_job,'date',run_date = datetime(self.meet_time.year,self.meet_time.month,self.meet_time.day,self.meet_time.hour,self.meet_time.minute,0),args=['text'],id="job")
            self.sched.start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainProgram()
    ui.show()
    sys.exit(app.exec_())