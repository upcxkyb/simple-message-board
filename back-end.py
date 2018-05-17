from flask import Flask
from flask import render_template
from flask import request
import smtplib, configparser
from email.mime.text import MIMEText
from email.header import Header

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/m')
def message():
    if request.method == 'GET':
        content = request.args.get('content')

        config = configparser.ConfigParser()
        config.read('info.ini')

        mail_host = config['Mail']['mail_host']
        mail_user = config['Mail']['mail_user']
        mail_pass = config['Mail']['mail_pass']
        
        sender = config['Mail']['sender']
        receivers = [config['Mail']['receivers']]
        
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = Header("信控易班工作站", 'utf-8')
        message['To'] =  Header("信息与控制工程学院办公室", 'utf-8')
        
        subject = '信息与控制工程学院-留言板'
        message['Subject'] = Header(subject, 'utf-8')
        
        try:
            smtpObj = smtplib.SMTP_SSL() 
            smtpObj.connect(mail_host, 465)
            smtpObj.login(mail_user,mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print ("邮件发送成功")
        except smtplib.SMTPException:
            print ("Error: 无法发送邮件")

        return render_template('sendok.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)