from email import encoders
from email.utils import parseaddr,formataddr
from email.mime.text import MIMEText
from email.header import Header

import smtplib
#smtp.qq.com （端口465或587）
#smtp.126.com 	 25 

def _format_addr(s):
    name,addr=parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))

def sendemail(to_addr,title,text):
    #server_port={'163':'25','qq':'587','126':'25'}
    #from_addr=input('From:')
    from_addr='15201710458@163.com'
    #password=input('Password:')
    password='159753Lf'

    #to_addr=input('To:')
    #to_addr='15201710458@163.com'

    #smtp_server=input('SMTP server:')
    #发信人端的smtp服务器
    smtp_server='smtp.163.com'

    msg=MIMEText('%s'%text,'plain','utf-8')
    msg['From']=_format_addr('系统管理员<%s>'%from_addr)
    msg['To']=_format_addr('用户<%s>'%to_addr)
    msg['Subject']=Header('%s'%title,'utf-8').encode()

    try:
        server=smtplib.SMTP(smtp_server,25)# no ssl port 465/994 #ssl port
        #server.starttls()#ssl safe Connection fail
        server.set_debuglevel(1)
        server.login(from_addr,password)
        to_list=to_addr.split(',')
        server.sendmail(from_addr,to_list,msg.as_string())
        print('sent it')
    except Exception as e:
        print(e)
        
    
    server.quit()
if __name__=='__main__':
    
    sendemail('505680497@qq.com,1462327302@qq.com,15201710458@163.com','test233','test233')