# 🔥Tencent-AutoMeeting🔥

Tencent-AutoMeeting是专用于网课期间的定时会议图形化项目，用于定时自动加入腾讯会议。

## 🔈功能特性

- 腾讯会议定时入会
- 使用网页端会议（VoovMeeting），不需要下载会议客户端
- 自动安装所需的chromedriver驱动

## 🥥部署说明

**环境要求**

Python 3.8.x

1. clone项目到本地

   ~~~
   git clone git@github.com:SummerFoam233/Tencent-AutoMeeting-GUI.git
   ~~~

2. 安装依赖库

   ~~~
   pip install -r requirements.txt
   ~~~

3. 运行程序

   ~~~
   python MainProgram.py
   ~~~

## 📚使用教程

1. 每次启动项目时会检查当前目录下的`chromedriver.exe`版本是否与浏览器对应，若不对应会自动更新。

   ![image-20221104033922379](https://summerfoam233-image.oss-cn-beijing.aliyuncs.com/img/2022/11/04/20221104033922.png)

2. 输入会议号，入会姓名和入会时间（不会检查会议号是否存在，请自行注意）。

![image-20221104033959495](https://summerfoam233-image.oss-cn-beijing.aliyuncs.com/img/2022/11/04/20221104033959.png)

3. 点击开始托管按钮，时间到时会自动通过浏览器入会。

![image-20221104034127191](https://summerfoam233-image.oss-cn-beijing.aliyuncs.com/img/2022/11/04/20221104034127.png)

## 😅下载说明

打包进行中...