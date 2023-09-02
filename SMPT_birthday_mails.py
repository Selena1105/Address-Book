# 实现功能：利用SMPT协议，向当日生日的联系人群发生日祝福邮件

import pandas as pd
import datetime
import smtplib
import email
from email.mime.text import MIMEText

# 负责构造图片
from email.mime.image import MIMEImage

# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header

# 获取当天生日名单

def selectPerson(df):
    # 获取所有人生日和邮箱

    birthdays = df['birthday'].values
    emails = df['email'].values

    # 找出当日生日的人，保存名字及邮箱

    email_list =[]
    today = datetime.datetime.now()
    for i in range(0, len(birthdays)):
        birthday = datetime.datetime.strptime(birthdays[i], "%m-%d")
        if birthday.month == today.month and birthday.day == today.day:
            email_list.append(str(emails[i]))
    print(email_list)

    return email_list


# 发送生日邮件（单人）
def sendMail(email_list):
    # SMTP服务器
    mail_host = "smtp.qq.com"

    # 发件人邮箱
    mail_sender = "267294230@qq.com"

    # 邮箱授权码
    mail_license = "nfnufobsgbcwcbcc"
    
        # 收件人邮箱
    mail_receivers = email_list

    # 设置邮件本体
    mail = MIMEMultipart('related')

    # 邮件主题
    subject_content = """生日祝福邮件"""

    # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
    mail["From"] = "senders<267294630@qq.com>"
    
    # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    mail["To"] = "receivers<@qq.com>"
    
    # 设置邮件主题
    mail["Subject"] = Header(subject_content,'utf-8')

    # 邮件正文内容
    body_content = """亲爱的朋友，生日快乐！"""
    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    message_text = MIMEText(body_content,"plain","utf-8")
    # 向MIMEMultipart对象中添加文本对象
    mail.attach(message_text)

    # 二进制读取图片
    image_data = open('birthday.jpg','rb')
    # 设置读取获取的二进制数据
    message_image = MIMEImage(image_data.read())
    # 关闭刚才打开的文件
    image_data.close()
    # 添加图片文件到邮件信息当中去
    mail.attach(message_image)

    # 创建SMTP对象
    stp = smtplib.SMTP()
    # 设置发件人邮箱的域名和端口，端口地址为25
    stp.connect(mail_host, 25)  
    # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
    stp.set_debuglevel(1)

    # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
    stp.login(mail_sender,mail_license)
    # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
    stp.sendmail(mail_sender, mail_receivers, mail.as_string())
    print("邮件发送成功")
    
    # 关闭SMTP对象
    stp.quit()




