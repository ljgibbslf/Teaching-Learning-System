import re

def get_email(test):
    email_reg=re.compile(r'(.*)@(\w+)\.com')
    email_match=email_reg.match(test)
    if email_match:
        print('ok!check the email:',email_match.group(1),email_match.group(2))
        return email_match.group(0)
                
    else:
        print('failed')
        return None

if __name__=='__main__':
    test=input('please input your email address:')
    get_email(test)