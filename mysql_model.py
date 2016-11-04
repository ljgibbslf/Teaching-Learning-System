#加载mysql库=====================================================
import mysql.connector

#连接数据库=======================================================
def connect_db():
    conn = mysql.connector.connect(host='#',user='##',
    password='#',database='intelligent_teaching_system')
    return conn
#you can use your own mysql db here and if you want my db,you contact me by 15201710458@163.com
 
#简单查询========================================================
def find_all_student():
    #查询所有学生
    conn=connect_db()
    cursor = conn.cursor()
    cursor.execute('select * from student')
    value=cursor.fetchall()
    print(value)
    cursor.close()
    conn.close()
    return value

def find_all_teacher():
    #查询所有教师
    conn=connect_db()
    cursor = conn.cursor()
    cursor.execute('select * from teacher')
    value=cursor.fetchall()
    print(value)
    cursor.close()
    conn.close()
    return value

def find_all_course():
    #查询所有课程
    conn=connect_db()
    cursor = conn.cursor()
    cursor.execute('select * from course')
    value=cursor.fetchall()
    print(value)
    cursor.close()
    conn.close()
    return value

def find_all_reward():
    #查询所有奖项
    conn=connect_db()
    cursor = conn.cursor()
    cursor.execute('select * from reward')
    value=cursor.fetchall()
    print(value)
    cursor.close()
    conn.close()
    return value

def find_all_seminar():
    #查询所有研讨
    conn=connect_db()
    cursor = conn.cursor()
    cursor.execute('select * from seminar')
    value=cursor.fetchall()
    print(value)
    cursor.close()
    conn.close()
    return value

#参数查询========================================================
def find_some_student(cond,regex=False):
    #数据库搜索函数
    #通过字典接收参数 进行参数查找以及排序指定学生 是否使用模糊查询默认为否 
    #得到的gpa数据为str 但不影响排序
    
    print(cond)#测试参数
    for x in cond:
        if cond.get(x)=='':
            cond[x]='%'
    #将空条件设定为%（mysql like语句中的通配符）
    if cond['student_gpa_max']=='%':
        cond['student_gpa_max']=4.0
    if cond['student_gpa_min']=='%':
        cond['student_gpa_min']=0.0
    #绩点比较特殊，默认为0-4
    if cond['up_or_down']=='down':
        cond['order']=cond['order']+' DESC'
    #读取升序/降序
    if cond['student_major']=='all':
        cond['student_major']='%'
    #默认所有专业

    conn=connect_db()
    cursor = conn.cursor()
    #连接数据库
    if regex==True:
        #模糊查询使用sql正则regexp语句 但只支持对名字进行模糊查询
        if cond['student_course']=='%':
            #课程sql语句比较特殊，需要区分默认无参及有参的情况
            sql='select * from student where STUDENT_ID like %s and STUDENT_NAME regexp %s and STUDENT_GPA between %s and %s '
            sql+='and STUDENT_COURSE like %s and STUDENT_REWARD like %s and STUDENT_GRADE=%s and STUDENT_MAJOR like %s and STUDENT_SEMINAR like %s order by '
        else:
            sql='select * from student where STUDENT_ID like %s and STUDENT_NAME like %s and STUDENT_GPA between %s and %s '
            sql+='and FIND_IN_SET(%s,student.STUDENT_COURSE) and STUDENT_REWARD like %s and STUDENT_GRADE=%s and STUDENT_MAJOR like %s and STUDENT_SEMINAR like %s order by '
    else:
        if cond['student_course']=='%':
            sql='select * from student where STUDENT_ID like %s and STUDENT_NAME like %s and STUDENT_GPA between %s and %s '
            sql+='and STUDENT_COURSE like %s and STUDENT_REWARD like %s and STUDENT_GRADE=%s and STUDENT_MAJOR like %s and STUDENT_SEMINAR like %s order by '
        else:
            sql='select * from student where STUDENT_ID like %s and STUDENT_NAME like %s and STUDENT_GPA between %s and %s '
            sql+='and FIND_IN_SET(%s,student.STUDENT_COURSE) and STUDENT_REWARD like %s and STUDENT_GRADE=%s and STUDENT_MAJOR like %s and STUDENT_SEMINAR like %s order by '
    cursor.execute( sql+cond['order'],(cond['student_id'],cond['student_name'],cond['student_gpa_min'],
    cond['student_gpa_max'],cond['student_course'],cond['student_reward'],cond['student_grade'],cond['student_major'],cond['student_seminar']))
    #order by 占位符不起作用 暂时用+连接字符串
    value=cursor.fetchall()
    #获得查询结果集
    count=0
    for x in value:
        count+=1
    #记录记录数量  
    cursor.close()
    conn.close()
    #关闭指针和数据库连接
    if count==0:
        return ''
    else:
        return value
    #返回结果
    
def find_some_course(cond,regex=False):
    #参数查询指定课程
    conn=connect_db()
    cursor = conn.cursor()
    for x in cond:
        if cond.get(x)=='':
            cond[x]='%'
    
    #cursor.execute('select * from course  INNER JOIN student ON course.COURSE_ID=student.STUDENT_COURSE OR FIND_IN_SET(course.COURSE_ID,
    #student.STUDENT_COURSE) where COURSE_ID=%s',(course_id,))
    if regex:
        #正则regexp
        sql='select * from course where COURSE_ID like %s and COURSE_NAME regexp %s and COURSE_TIME like %s and COURSE_LOCATION like %s'
    else:
        sql='select * from course where COURSE_ID like %s and COURSE_NAME like %s and COURSE_TIME like %s and COURSE_LOCATION like %s'

    cursor.execute(sql,(cond['course_id'],cond['course_name'],cond['course_time'],cond['course_location']))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    if count==0:
        return ''
    else:
        return value

def find_some_teacher(cond,regex=False):
    #参数查询指定教师
    conn=connect_db()
    cursor = conn.cursor()
    #print(cond)
    for x in cond:
        if cond.get(x)=='':
            cond[x]='%'
    if 'up_or_down' in cond:
        if cond['up_or_down']=='down':
            cond['order']=cond['order']+' DESC'
    
    #print(cond)
    if regex:
        #正则regexp
        if cond['teacher_course']=='%':
            sql='select * from teacher where TEACHER_ID like %s and TEACHER_NAME regexp %s and TEACHER_SEMINAR like %s and TEACHER_COURSE like %s and TEACHER_SEMINAR like %s and TEACHER_COLLEGE like %s order by  '
        else:    
            sql='select * from teacher where TEACHER_ID like %s and TEACHER_NAME like %s and TEACHER_SEMINAR like %s and FIND_IN_SET(%s,teacher.TEACHER_COURSE) and TEACHER_SEMINAR like %s and TEACHER_COLLEGE=%s order by  '

    else:        
        if cond['teacher_course']=='%':
            sql='select * from teacher where TEACHER_ID like %s and TEACHER_NAME like %s and TEACHER_SEMINAR like %s and TEACHER_COURSE like %s and TEACHER_SEMINAR like %s and TEACHER_COLLEGE  like %s order by  '
        else:    
            sql='select * from teacher where TEACHER_ID like %s and TEACHER_NAME like %s and TEACHER_SEMINAR like %s and FIND_IN_SET(%s,teacher.TEACHER_COURSE) and TEACHER_SEMINAR like %s and TEACHER_COLLEGE like %s order by  '

    cursor.execute(sql+cond['order'],(cond['teacher_id'],cond['teacher_name'],cond['teacher_seminar'],cond['teacher_course'],cond['teacher_seminar'],cond['teacher_college']))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    if count==0:
        return ''
    else:
        return value

def find_some_seminar(cond,regex=False):

    #参数查询指定研讨活动
    conn=connect_db()
    cursor = conn.cursor()
    #print(cond)
    for x in cond:
        if cond.get(x)=='':
            cond[x]='%'
    
    #print(cond)
    if regex:
        #正则regexp
        if cond['seminar_student_id']=='%':
            sql='select * from seminar where SEMINAR_ID like %s and SEMINAR_NAME regexp %s and SEMINAR_STUDENT_ID like %s and SEMINAR_TEACHER_ID like %s'
        else:  
            sql='select * from seminar where SEMINAR_ID like %s and SEMINAR_NAME regexp %s and FIND_IN_SET(%s,seminar.SEMINAR_STUDENT_ID) and SEMINAR_TEACHER_ID like %s'

    else:        
        if cond['seminar_student_id']=='%':
            sql='select * from seminar where SEMINAR_ID like %s and SEMINAR_NAME like %s and SEMINAR_STUDENT_ID like %s and SEMINAR_TEACHER_ID like %s'
        else:  
            sql='select * from seminar where SEMINAR_ID like %s and SEMINAR_NAME like %s and FIND_IN_SET(%s,seminar.SEMINAR_STUDENT_ID) and SEMINAR_TEACHER_ID like %s'

    cursor.execute(sql,(cond['seminar_id'],cond['seminar_name'],cond['seminar_student_id'],cond['seminar_teacher_id']))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    if count==0:
        return ''
    else:
        return value

def find_some_reward(cond,regex=False):

    #参数查询指定奖项
    conn=connect_db()
    cursor = conn.cursor()
    #print(cond)
    for x in cond:
        if cond.get(x)=='':
            cond[x]='%'
    
    #print(cond)
    if regex:
        #正则regexp
        if cond['reward_student_id']=='%':
            sql='select * from reward where REWARD_ID like %s and REWARD_NAME regexp %s and REWARD_STUDENT_ID like %s '
        else:  
            sql='select * from reward where REWARD_ID like %s and REWARD_NAME regexp %s and FIND_IN_SET(%s,reward.REWARD_STUDENT_ID) '

    else:        
        if cond['reward_student_id']=='%':
            sql='select * from reward where REWARD_ID like %s and REWARD_NAME like %s and REWARD_STUDENT_ID like %s '
        else:  
            sql='select * from reward where REWARD_ID like %s and REWARD_NAME like %s and FIND_IN_SET(%s,reward.REWARD_STUDENT_ID) '

    cursor.execute(sql,(cond['reward_id'],cond['reward_name'],cond['reward_student_id']))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    if count==0:
        return ''
    else:
        return value
#登陆/注册=======================================================
def register(name,pwd):
    #
    conn=connect_db()
    cursor=conn.cursor()
    if check_id(name) is False:
        return False
    
    sql='insert into user values (%s,%s)'
    
    result=cursor.execute(sql,(name,pwd))
    cursor.close()
    conn.commit()
    conn.close()
    return True

def check_id(id):
    
    conn=connect_db()
    cursor=conn.cursor()
    sql='select ID from user'
    cursor.execute(sql)
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    #print(value)
    for x in value:
        if x[0]==id:
            return False
    return True

def login(name,pwd):
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select ID,PASSWORD from user where ID=%s'
    cursor.execute(sql,(name,))
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    print(value)
    if not len(value)==0:
        if value[0][1]==pwd:
            return value[0][0]
    return 0

#需求查询（因为上面的参数查询的耦合性过强）=========================
def find_teacher_id(teacher_id):
    #通过教师号查询教师
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select * from teacher where TEACHER_ID=%s'
    cursor.execute(sql,(teacher_id,))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    if count==0:
        return ''
    else:
        return value
    return 0

def find_student_id(student_id):
    #通过学生号查询学生
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select * from student where STUDENT_ID=%s'
    cursor.execute(sql,(student_id,))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    if count==0:
        return ''
    else:
        return value
    return 0

def find_course_list(course_id):
    #通过课程号查询课程
    conn=connect_db()
    cursor=conn.cursor()
    value=[]
    for x in course_id:
        sql='select * from course where COURSE_ID=%s'
        cursor.execute(sql,(x,))
        value+=cursor.fetchall()
    cursor.close()
    conn.close()
    return value

def find_student_course(course_id):
    #查询上某门课程的学生
    conn=connect_db()
    cursor=conn.cursor()
    
    #sql='select * from student where FIND_IN_SET(%s,student.STUDENT_COURSE)'
    sql='SELECT student.STUDENT_ID,student.STUDENT_NAME,student.STUDENT_GRADE,student.STUDENT_MAJOR,student.STUDENT_EMAIL,student.STUDENT_PHONE_NUM,student.STUDENT_GPA,'
    sql+='student.STUDENT_COURSE,absence.ABSENCE_COUNT,absence.ABSENCE_TIME FROM student LEFT JOIN absence ON absence.STUDENT_ID = student.STUDENT_ID where FIND_IN_SET(%s,student.STUDENT_COURSE)'
    cursor.execute(sql,(course_id,))
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    return value

def find_student_course_order(course_id,teacher_id,order='student.STUDENT_GPA DESC'):
    #查询上某门课程的学生_排序
    if order=='student_id':
        order='student.'+order.upper()
    else:
        order='student.'+order.upper()+' DESC'
    

    conn=connect_db()
    cursor=conn.cursor()
    
    #sql='select * from student where FIND_IN_SET(%s,student.STUDENT_COURSE)'
    sql='SELECT student.STUDENT_ID,student.STUDENT_NAME,student.STUDENT_GRADE,student.STUDENT_MAJOR,student.STUDENT_EMAIL,student.STUDENT_PHONE_NUM,student.STUDENT_GPA,'
    sql+='student.STUDENT_COURSE,absence.ABSENCE_COUNT,absence.ABSENCE_TIME FROM student LEFT JOIN absence ON absence.STUDENT_ID = student.STUDENT_ID where FIND_IN_SET(%s,student.STUDENT_COURSE) order by '
    cursor.execute(sql+order,(course_id,))
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    return value

def find_student_course_rate(course_id,teacher_id):
    #查询上某门课程的学生_排序(显示教师评价)
    conn=connect_db()
    cursor=conn.cursor()
    
    #sql='select * from student where FIND_IN_SET(%s,student.STUDENT_COURSE)'
    sql='SELECT student.STUDENT_ID,student.STUDENT_NAME,rate.SCORE,rate.RATE,rate.TEACHER_ID,rate.COURSE_ID '
    sql+='FROM student RIGHT JOIN rate ON student.STUDENT_ID = rate.STUDENT_ID WHERE rate.TEACHER_ID=%s and FIND_IN_SET(%s,rate.COURSE_ID) order by rate.SCORE'
    
    cursor.execute(sql,(teacher_id,course_id))
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    return value

def find_student_ordinary(course_id):
    #显示平时成绩
    conn=connect_db()
    cursor=conn.cursor()
    
    #sql='select * from student where FIND_IN_SET(%s,student.STUDENT_COURSE)'
    sql='SELECT student.STUDENT_ID,student.STUDENT_NAME,ordinary.ORDINARY_SCORE FROM ordinary right JOIN student ON student.STUDENT_ID = ordinary.STUDENT_ID WHERE ordinary.COURSE_ID=%s'

    cursor.execute(sql,(course_id,))
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    return value

def find_teacher_course(course_id):
    #查询上某门课程的教师
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select * from teacher where FIND_IN_SET(%s,teacher.TEACHER_COURSE)'
    cursor.execute(sql,(course_id,))
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    return value
#平时成绩=============================================================
def ordinary_score(student_id,course_id,score):
    #写入平时成绩
    conn=connect_db()
    cursor=conn.cursor()
    print(check_dup_student(int(student_id),course_id,'ordinary'))
    if check_dup_student(int(student_id),int(course_id),'ordinary'):
        #如果没有成绩则新建行 不然就修改原本的成绩
        sql='insert into ordinary values (%s,%s,%s,%s)'
        result=cursor.execute(sql,(student_id,course_id,score,'暂未上传'))
    else:
        sql='update ordinary set ORDINARY_SCORE=%s where STUDENT_ID=%s and COURSE_ID=%s'
        result=cursor.execute(sql,(score,student_id,course_id))

    cursor.close()
    conn.commit()
    conn.close()
    return result

def check_dup_student(student_id,course_id,table_name):
    #查询是否有过纪录
    conn=connect_db()
    cursor=conn.cursor()
    if table_name=='ordinary':
        sql='select STUDENT_ID,COURSE_ID from ordinary'
    elif table_name=='absence':
        sql='select STUDENT_ID,COURSE_ID from absence'
    else:
        sql=''

    cursor.execute(sql)
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    for x in value:
        if x[0]==student_id and x[1]==course_id:
            return False
    return True

#作业分数=============================================================
def homework_score(student_id,course_id,score):
    #写入作业成绩(同在ordinary表中)
    conn=connect_db()
    cursor=conn.cursor()
    print(check_dup_student(int(student_id),course_id,'ordinary'))
    if check_dup_student(int(student_id),int(course_id),'ordinary'):
        #如果没有成绩则新建行 不然就修改原本的成绩
        sql='insert into ordinary values (%s,%s,%s,%s)'
        result=cursor.execute(sql,(student_id,course_id,'暂未上传',score))
    else:
        sql='update ordinary set HOMEWORK_SCORE=%s where STUDENT_ID=%s and COURSE_ID=%s'
        result=cursor.execute(sql,(score,student_id,course_id))

    cursor.close()
    conn.commit()
    conn.close()
    return result


#纪录缺勤（用到上面的查重函数）=========================================
def student_absence(student_id,course_id,absence_time,count):
    conn=connect_db()
    cursor=conn.cursor()
    if check_dup_student(int(student_id),int(course_id),'absence'):
        sql='insert into absence values (%s,%s,%s,%s)'
        result=cursor.execute(sql,(student_id,course_id,absence_time,count))
    else:
        sql='update absence set ABSENCE_TIME=%s,ABSENCE_COUNT=%s where STUDENT_ID=%s and COURSE_ID=%s'
        result=cursor.execute(sql,(absence_time,count,student_id,course_id))

    cursor.close()
    conn.commit()
    conn.close()
    return result


#评价教师=============================================================
def rate_teacher(student_id,teacher_id,course_id,rate,score):
    conn=connect_db()
    cursor=conn.cursor()
    if check_dup_teacher(int(student_id),int(teacher_id),int(course_id)):
        sql='insert into rate values (%s,%s,%s,%s,%s)'
        result=cursor.execute(sql,(student_id,teacher_id,course_id,rate,score))
    else:
        sql='update rate set RATE=%s,SCORE=%s where STUDENT_ID=%s and TEACHER_ID=%s and COURSE_ID=%s'
        result=cursor.execute(sql,(rate,score,student_id,teacher_id,course_id))

    cursor.close()
    conn.commit()
    conn.close()
    return result


def check_dup_teacher(student_id,teacher_id,course_id):
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select STUDENT_ID,TEACHER_ID,COURSE_ID from rate'
    cursor.execute(sql)
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    for x in value:
        if x[0]==student_id and x[1]==teacher_id and x[2]==course_id:
            return False
    return True

#查询历史成绩===========================================================
def find_history_score(student_id):
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select * from score where STUDENT_ID=%s'
    cursor.execute(sql,(student_id,))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    if count==0:
        return ''
    else:
        return value
    return 0
#创建研讨=================================================
def insert_seminar(name,teacher_id,location,time):
    conn=connect_db()
    cursor=conn.cursor()
    student='招募中'
    sql='insert into seminar values (%s,%s,%s,%s,%s,%s)'
    
    result=cursor.execute(sql,(get_last_id()+1,name,teacher_id,time,location,student))
    cursor.close()
    conn.commit()
    conn.close()
    return result

def get_last_id():
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select SEMINAR_ID from seminar '
    cursor.execute(sql)
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    
    return value[count-1][0]
#消息系统=================================================
def get_message(receiver_id):
    #返回最新的三条消息（to do 未读）
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select * from message where RECEIVER_ID=%s'
    cursor.execute(sql,(receiver_id,))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    if count==0:
        return False
    elif count>=3:
        return value[-3:]
    else:
        return value

def insert_message(receiver_id,sender_id,message):
    #写入消息
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='insert into message values (%s,%s,%s,%s)'
    
    result=cursor.execute(sql,(int(receiver_id),int(sender_id),message,'f'))
    cursor.close()
    conn.commit()
    conn.close()
    return result

def get_all_message(receiver_id):
    #所有消息内容
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select * from message where RECEIVER_ID=%s'
    cursor.execute(sql,(receiver_id,))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    return value

def not_read_message_num(receiver_id):
    #返回未读消息的数量
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='select * from message where RECEIVER_ID=%s and IS_READ=%s'
    cursor.execute(sql,(int(receiver_id),'f'))
    value=cursor.fetchall()
    count=0
    for x in value:
        count+=1
       
    cursor.close()
    conn.close()
    #print(count)
    return count

def set_message_read(receiver_id):
    #现阶段数据表设置无法实现对某条消息已读
    #将所有消息标记为已读
    conn=connect_db()
    cursor=conn.cursor()

    sql='update message set IS_READ =%s where RECEIVER_ID=%s'
    
    result=cursor.execute(sql,('t',int(receiver_id)))
    cursor.close()
    conn.commit()
    conn.close()
    return result

def set_message_not_read(receiver_id):
    #现阶段数据表设置无法实现对某条消息操作
    #将所有消息标记为未读
    conn=connect_db()
    cursor=conn.cursor()

    sql='update message set IS_READ =%s where RECEIVER_ID=%s'
    
    result=cursor.execute(sql,('f',int(receiver_id)))
    cursor.close()
    conn.commit()
    conn.close()
    return result

def delete_all_message(receiver_id):
    #删除所有消息(设想通过改掉收信人实现 这样还能恢复)
    conn=connect_db()
    cursor=conn.cursor()

    sql='update message set RECEIVER_ID =%s where RECEIVER_ID=%s'
    
    result=cursor.execute(sql,(int(receiver_id)+10000000,int(receiver_id)))
    cursor.close()
    conn.commit()
    conn.close()
    return result

def all_course_message(course_id,sender_id,message):
    #向全班所有学生发送站内信
    conn=connect_db()
    cursor=conn.cursor()
    
    #sql='select * from student where FIND_IN_SET(%s,student.STUDENT_COURSE)'
    sql='SELECT student.STUDENT_ID FROM student where FIND_IN_SET(%s,student.STUDENT_COURSE)'
    cursor.execute(sql,(course_id,))
    value=cursor.fetchall()

    sql_insert='insert into message values (%s,%s,%s,%s)'
    for x in value:
        #print(x[0])
        cursor.execute(sql_insert,(int(x[0]),int(sender_id),message,'f'))
    conn.commit()  
    cursor.close()
    conn.close()


#读取邮箱功能==============================================
def get_course_all_email(course_id):
    #获取全班同学的邮箱
    conn=connect_db()
    cursor=conn.cursor()

    sql='select STUDENT_EMAIL from student where FIND_IN_SET(%s,student.STUDENT_COURSE)'

    cursor.execute(sql,(course_id,))
    value=cursor.fetchall()
    cursor.close()
    conn.close()
    #返回一个list
    email_list=''
    for x in value:
        email_list+=x[0]+','
    return email_list[:-1]
    

#收集意见反馈==============================================
def insert_advice(email,advice):
    conn=connect_db()
    cursor=conn.cursor()
    
    sql='insert into advice values (%s,%s)'
    
    result=cursor.execute(sql,(email,advice))
    cursor.close()
    conn.commit()
    conn.close()
    return result

#显示修改个人信息=============================================


#测试函数===============================================================
if __name__=='__main__':
    #find_all_student()
    #find_some_student('','','','')
    #print(login('1003','159753'))
    #print(find_teacher_course('1001'))
    #print(find_teacher_course(['1001','1002']))
    #print(find_student_course('1001'))
    #ordinary_score("14120001",1001,90)
    #print(check_dup_student(14120001,1001))
    #print(register('14120003','159753'))
    #print(check_id('14120003'))
    #print(get_last_id())
    #print(get_message(1001))
    
    #email_list=''
    #for x in get_course_all_email('1001'):
    #   email_list+=x[0]+','
    #print(email_list[:-1])
    
    #print(not_read_message_num('14120003'))
    #print(set_message_not_read('14120003'))
    
    #for x in get_all_message('1001'):
    #   print(x)
    #delete_all_message('14120002')
    all_course_message('1005','1001','test')
