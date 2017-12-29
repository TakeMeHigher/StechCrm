#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

msg = MIMEText('老大，我今天需要请假。', 'plain', 'utf-8')  # 发送内容
msg['From'] = formataddr(["武沛齐", 'xxxx@126.com'])  # 发件人
msg['To'] = formataddr(["习大大", 'ooooo@qq.com'])  # 收件人
msg['Subject'] = "【请回复】元旦请假事宜"  # 主题

server = smtplib.SMTP("smtp.126.com", 25) # SMTP服务
server.login("xxxx@126.com", "密码") # 邮箱用户名和密码
server.sendmail('xxxx@126.com', ['ooooo@qq.com', ], msg.as_string()) # 发送者和接收者
server.quit()



