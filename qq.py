# import smtplib
# from email.mime.text import MIMEText
# _user = "你的qq邮箱"
# _pwd  = "你的授权码"
# _to   = "501257367@163.com"
#
# msg = MIMEText("Test")
# msg["Subject"] = "don't panic"
# msg["From"]    = _user
# msg["To"]      = _to
#
# try:
#     s = smtplib.SMTP_SSL("smtp.qq.com ", 465)
#     s.login(_user, _pwd)
#     s.sendmail(_user, _to, msg.as_string())
#     s.quit()
#     print("Success!")
# except smtplib.SMTPException as e:
#     print("Falied,%s" % e)




import smtplib
from email.mime.text import MIMEText
import string

#第三方SMTP服务
mail_host = "smtp.qq.com"           # 设置服务器
mail_user = "492745473@qq.com"        # 用户名
mail_pwd  = "zglmzcyjsvppbhic"      # 口令,QQ邮箱是输入授权码，在qq邮箱设置 里用验证过的手机发送短信获得，不含空格
mail_to  = ['1789920207@qq.com',]     #接收邮件列表,是list,不是字符串

#邮件内容
msg = MIMEText("傻叉")      # 邮件正文
msg['Subject'] = "大傻叉"     # 邮件标题
msg['From'] = mail_user        # 发件人
msg['To'] = ','.join(mail_to)         # 收件人，必须是一个字符串

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    #smtpObj = smtplib.SMTP(mail_host, 25)

    smtpObj.login(mail_user, mail_pwd)
    smtpObj.sendmail(mail_user,mail_to, msg.as_string())
    smtpObj.quit()
    print("邮件发送成功!")
except smtplib.SMTPException:
    print ("邮件发送失败!")

