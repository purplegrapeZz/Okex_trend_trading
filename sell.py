# -*- coding: utf-8 -*-
from main import clear
from main import consts
import smtplib #登录发送退出
from email.mime.text import MIMEText

if __name__ == '__main__':
	try:
		clear.clear()
		import smtplib #登录发送退出
		from email.mime.text import MIMEText
		mail_host = nmsl.mail_host
		mail_user = nmsl.mail_user
		mail_pwd = nmsl.mail_pwd
		mail_receiver = nmsl.mail_receiver

		mail_subject = '清仓成功!'
		mail_content = '全部卖出成功!详情请查看日志~'
		msg = MIMEText(mail_content,'html','utf-8')
		msg['Subject'] = mail_subject
		msg['From'] = mail_user

		msg['To'] = mail_receiver
		client = smtplib.SMTP_SSL(mail_host,465) #得到smtp服务器的连接
		client.login(mail_user,mail_pwd) #登录
		client.send_message(msg)
		client.quit

	except Exception as err:
		import smtplib #登录发送退出
		from email.mime.text import MIMEText
		mail_host = nmsl.mail_host
		mail_user = nmsl.mail_user
		mail_pwd = nmsl.mail_pwd
		mail_receiver = nmsl.mail_receiver

		mail_subject = '报警提醒!程序异常退出!'
		mail_content = '错误提示:</br>%s'%err
		msg = MIMEText(mail_content,'html','utf-8')
		msg['Subject'] = mail_subject
		msg['From'] = mail_user

		msg['To'] = mail_receiver
		client = smtplib.SMTP_SSL(mail_host,465) #得到smtp服务器的连接
		client.login(mail_user,mail_pwd) #登录
		client.send_message(msg)
		client.quit



















