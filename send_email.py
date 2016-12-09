# __author__ = 'zhouyang'
# -*- coding: utf-8 -*-

from email.header import Header
from email.mime.text import MIMEText
import smtplib

# 导入配置文件，内部有邮箱配置信息
from Config import *


# 发送邮件的程序，需要指定主题和邮件的内容
def send_email(subject, text, from_addr=From_addr, to_addr=To_addr, smtp_server=Smtp_server, password=Password):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = Header(subject, 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
