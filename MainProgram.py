from PyQt5 import QtCore, QtGui, QtWidgets,QtMultimedia,QtMultimediaWidgets
from mainwindow import Ui_MainWindow
from loading import Ui_LoadingWindow
from PyQt5.QtCore import *
import time
from selenium import webdriver
import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.common.by import By
import os
import re
import winreg
import zipfile
import requests
from selenium.common.exceptions import NoSuchElementException      
from pyautogui import write as pag_write

class LoadWin(QtWidgets.QMainWindow,Ui_LoadingWindow):
    def __init__(self,parent=None):
        super(LoadWin,self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint) # 无边框化和窗口置顶
        self.mainwindow = MainProgram()
        self.timer = QBasicTimer()
        self.step = 0
        self.process_run()
        
    def process_run(self):
        self.checkthread = UpdateCheckThread(self.LoadingMessageLb)
        self.checkthread.part_signal.connect(self.process_set_part)
        self.checkthread.finish_signal.connect(self.show_main_win)
        self.checkthread.start()
        
    def process_set_part(self,num):
        self.step = num
        self.progressBar.setValue(self.step)
        if num == 0:
            self.timer.start(100,self)
        if num == 1:
            self.timer.stop()
            self.timer.start(10,self)
            self.LoadingMessageLb.setText("完成更新检查，等待主界面加载>>>")
        if num == 2:
            self.timer.stop()

    def timerEvent(self, *args, **kwargs):
        self.progressBar.setValue(self.step)
        if self.step < 100:
            self.step += 1
            
    def show_main_win(self):
        self.mainwindow.show()
        self.close()
        
class MainProgram(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainProgram,self).__init__(
            parent)
        self.setupUi(self)
        self.ClickEvent()
        self.StartTimeLE.setText(datetime.now().strftime("%Y/%m/%d/%H:%M"))
        self.meeting_data = QSettings('config.ini',QSettings.IniFormat)
        self.meeting_data.setIniCodec('UTF-8')
    
    def QtMessageBox(self,state,str_1,str_2,delay=2):
        if state.lower() == 'information':
            Messagebox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,str_1,str_2)
        elif state.lower() == 'warning':
            Messagebox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,str_1,str_2)
        elif state.lower() == 'critical':
            Messagebox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,str_1,str_2)
        Messagebox.setWindowIcon(QtGui.QIcon('icons/logo.png'))
        self.msgtimer = QTimer()
        self.msgtimer.timeout.connect(lambda: Messagebox.close() and self.msgtimer.stop())
        self.msgtimer.start(delay*1000)
        Messagebox.exec_()
        return None
        
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
        meeting_ID = self.IDComBox.currentText()
        meeting_Name = self.NameComBox.currentText()
        meeting_Password = self.PasswdComBox.currentText()
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
            
        self.webthread = WebThread(meeting_ID,meeting_Name,meeting_Password,ontime_flag,meet_time)
        self.webthread.finish_signal.connect(self.task_finish_event)
        self.webthread.start()
    
    def task_finish_event(self,num):
        if num == 0:
            self.QtMessageBox("information","提示","托管任务已完成!")
        if num == 1:
            self.QtMessageBox("warning","警告","托管失败，请核实入会密码后重新托管!")
            
class UpdateCheckThread(QtCore.QThread):
    part_signal = pyqtSignal(int) # 进度环节信号
    finish_signal = pyqtSignal(int) # 结束传递信号
    
    def __init__(self,LoadingMessageLb):
        super().__init__()
        self.TextLb = LoadingMessageLb
        self.base_url = 'http://npm.taobao.org/mirrors/chromedriver/'
        self.version_re = re.compile(r'^[1-9]\d*\.\d*.\d*')  # 匹配前3位版本号的正则表达式
        
    def getChromeVersion(self):
        """通过注册表查询chrome版本"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Google\\Chrome\\BLBeacon')
            value, t = winreg.QueryValueEx(key, 'version')
            return self.version_re.findall(value)[0]  # 返回前3位版本号
        except WindowsError as e:
            self.part_signal.emit(2)
            self.TextLb.setStyleSheet("color:rgb(255, 43, 15)")
            self.TextLb.setText("未安装chrome浏览器，请安装后重试!")
            # 5秒后退出程序
            time.sleep(5)
            os._exit(0)
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

        download_url = f"{self.base_url}{latest_version}/chromedriver_win32.zip"
        file = requests.get(download_url)
        with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
            zip_file.write(file.content)
        # 解压
        f = zipfile.ZipFile("chromedriver.zip", 'r')
        for file in f.namelist():
            f.extract(file)

    def checkChromeDriverUpdate(self):
        
        self.TextLb.setText("正在检查chrome版本...")
        chrome_version = self.getChromeVersion()
        self.TextLb.setText("正在检查chromedriver版本...")
        driver_version = self.getChromeDriverVersion()
        self.TextLb.setText("正在核实版本是否对应...")
        if chrome_version == driver_version:
            # 版本一致，无需更新
            return
        self.TextLb.setText("chromedriver版本与chrome浏览器不兼容，更新中>>>")
        try:
            self.getLatestChromeDriver(chrome_version)
            self.TextLb.setText("chromedriver版本更新完毕!")
            os.remove("chromedriver.zip")
        except requests.exceptions.Timeout:
            self.TextLb.setStyleSheet("color:rgb(255, 43, 15)")
            self.TextLb.setText("chromedriver下载失败，请检查网络后重试!")
            self.part_signal.emit(2)
            time.sleep(5)
            os._exit(0)
        except Exception as e:
            self.TextLb.setStyleSheet("color:rgb(255, 43, 15)")
            self.TextLb.setText("chromedriver未知原因更新失败: {}".format(e))
            self.part_signal.emit(2)
            time.sleep(5)
            os._exit(0)
            
    def run(self):
        self.part_signal.emit(0)
        self.checkChromeDriverUpdate()
        self.part_signal.emit(1)
        time.sleep(1.5) # 模拟主界面加载时间
        self.finish_signal.emit(1)
        
class WebThread(QtCore.QThread):
    finish_signal = pyqtSignal(int) # 结束传递信号
    def __init__(self,meeting_ID,meeting_Name,meeting_Password,ontime_flag,meet_time):
        super().__init__()
        self.meeting_ID = meeting_ID
        self.meeting_Name = meeting_Name
        self.meeting_Password = meeting_Password
        self.ontime_flag = ontime_flag
        self.meet_time = meet_time
        self.sched = BlockingScheduler()
        self.driver_path = r"chromedriver.exe"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")  # 隐身模式打开
        self.driver = webdriver.Chrome(self.driver_path, options=self.options)
    
    # 判断是否存在该元素
    def isElementPresent(self, by, value):
        try:
            element =self.driver.find_element(by=by, value=value)
        except NoSuchElementException as e:
    # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return  False
        else:
    # 没有发生异常，表示在页面中找到了该元素，返回True
            return  True 
        
    def run_job(self,text):
        self.driver.get("https://voovmeeting.com/r")
        time.sleep(3)
        self.driver.find_elements_by_class_name("join-form__input")[0].send_keys(self.meeting_ID)
        self.driver.find_elements_by_class_name("join-form__input")[1].send_keys(self.meeting_Name)
        self.driver.find_element_by_css_selector(".tea-btn").click()
        time.sleep(3)
        self.driver.switch_to.frame(0)
        self.driver.find_element_by_css_selector(".met-btn").click()
        self.driver.find_element_by_css_selector(".met-checkbox").click()
        self.driver.find_element_by_css_selector(".met-btn").click()
        time.sleep(2)
        # 密码输入（如果有）
        if self.isElementPresent(By.CSS_SELECTOR,".tea-input-password"):
            self.driver.find_element_by_css_selector(".tea-input-password").click()
            print(self.meeting_Password)
            pag_write(self.meeting_Password)
            self.driver.find_element_by_css_selector(".dialog-btn:last-child").click()
            time.sleep(5)
            if self.isElementPresent(By.CSS_SELECTOR,".tea-form__help-text"):
                self.finish_signal.emit(1)
                return None
            else:
                Meeting_Text = self.driver.find_element_by_xpath('//*[@id="tea-overlay-root"]/div/div[1]').text
        self.finish_signal.emit(0)
        
    def run(self):
        if self.ontime_flag:
            self.run_job(None)
        else:
            self.sched.add_job(self.run_job,'date',run_date = datetime(self.meet_time.year,self.meet_time.month,self.meet_time.day,self.meet_time.hour,self.meet_time.minute,0),args=['text'],id="job")
            self.sched.start()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = LoadWin()
    ui.show()
    sys.exit(app.exec_())