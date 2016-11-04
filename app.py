import logging
import os

from flask import (Flask, make_response, redirect, render_template, request,
                   send_from_directory, session, url_for)
#自有包
from werkzeug import secure_filename

import bing_api
import email_regex
import mysql_model
#导入第三方库
import send_email

#导入自己写的库

#文件架构=========================================
#teaching_system
#   /static
#       /css
#       /font
#       /js
#   /templates
#       /teacher
#           course-student.html
#           course-work.html
#           index.html
#           message-course.html
#           ordinary-score.html
#           seminar.html
#           student-absence.html
#           teacher-course.html
#       /student
#           index.html
#           online-learn.html
#           student-homework.html
#           student-result.html
#           teacher-rate.html
#       home.html
#       base.html
#       base-teacher.html
#       base-student.html
#       feedback.html
#
#   app.py
#   send_eamail.py
#   email_regex.py
#   mysql_model.py

#感想=============================================
#404 一般都是哪打错了。。

#施工记录========================================
#send_email:用我的邮箱发送邮件 email_regex:邮件地址检查(基础)mysql_model:连接阿里云上的mysql数据库
#0.0.1 (16.9.19)  完成发送邮件模块的50%(基础发送功能，基础识别错误邮件地址功能，基础发送报错功能, 可选发送给个人和全部(施工中)
#                 完成基础邮件发送表单,*消除了只能发给自己的BUG。。。
#0.0.2 (16.9.20)  连接数据库，简单查询所有人，完成简单参数查询  
#0.0.3 (16.9.21)  继续施工参数查询，明确查询反馈(结果行数为0时提示),优化router接受的url ，设置了base模板     
#                 问题：读取表单的gpa数据一直失败(疑似解决 原因是表单中名字填错)
#                 有待了解SQL模糊查询
#0.0.4(16.9.22)   继续施工参数查询 完工全部查询(但order by 不明原因占位符失效，暂时用拼接字符串的简陋方法)
#                 部署完成学生几项查询 有待施工教师，课程参数查询  暂时确定两个入口(老师和学生)的计划以及登录界面 考虑制作视频介绍功能
#                 有待加深SQL语句知识 计划施工多表联合查询 优化mysql_model 改变sql查询为字典传参
#0.0.5(16.9.23)   发现BUG：发送邮件 在表单未填的情况下 返回400(已解决 因为checked写成check 导致没有默认项 顺手解决收信人为空时发送的BUG)；
#                 完成部分跨表查询
#0.0.6(16.9.24)   给教师，课程查询配备对应的表格标题,统一替换所有class，lesson为course 因为class会影响关键字;使用字典传送sql查找函数的参数
#0.0.7(16.9.25)   使用生成器生成字典 修复昨天误把字典设成列表的错误；草创注册界面 但写入数据库失败(原因是没有commit) 基本完成参数查询
#0.0.8(16.9.27)   加入登陆检验 继续完善内容  
#0.0.1(16.9.28)   进入0.1版本
#0.1.1(16.9.28)   进入新版本(虽然都是我自己决定的)显示当前登录的用户； 加入教师的课程管理，草创对课程内的学生进行管理(记录缺勤，迟到？，记录平时成绩？)email联系(未完成)
#                 代码越来越乱了 尤其是函数名 而且许多函数是否改成可复用不确定 有些函数耦合性过强；
#                 接下来再完善老师的部分 以及完成相应的学生部分(查看自己的课程，查看上课的老师，联系老师)(尚未决定是否学生教师账户隔离)
#                 需要继续学习 动态生成(灵活组建url)；担忧登录逻辑的可靠性 继续学习session 考虑多行数据的分页问题
#0.1.2(16.9.29)   新增了联系作者 也考虑用这个思路做联系老师/学生；修复邮件BUG 制作完成部分学生；正在全力制作文件上传系统(完成了部分)；重写了404页面
#                 装上了pylink 还不错
#0.1.3(16.9.30)   计划施工联系学生/教师 完成基本作业上传
#0.1.4(16.10.1)   整理一下app.py中的代码 基本完成联系教师/学生 自动填充邮件地址 
#                 接下来的任务：模糊查询 ，老师统一/单独查看作业 并评分 ，教师纪录出勤(形式还没想好)学生评价老师(课程)，竞赛 研讨 奖项的页面
#0.1.5(16.10.2)   初步完成纪录缺勤的前端页面(暂时没有数据库连接) 使用session随时存储和调出当前的课程号(还可以用于其他方面，即所谓上下文)增加联系课程全体学生的选项(暂时只有选项而已)
#0.1.6(16.10.3)   发现BUG：学生上传文件时 如果文件名是纯中文则会失去文件名(混合则失去所有中文) 完成教师查看全班学生作业的功能
#0.1.7(16.10.4)   完成登记平时成绩的前端页面(分为班级/个人两种登记方式;对mysql_model稍加整理;完成平时成绩(两种方式)的数据库写入;草创教师/学生登录分隔 即登录后即进入各自首页(其实没有分离)；修正了一个微小的BUG
#0.1.8(16.10.5)   部分完成了缺勤纪录的数据库写入 但出现了会使数据库出现问题的BUG(使用逗号分隔数据，第二次覆盖写入会使值变成0 此后连接数据库就会超时)
#                 BUG更新：去掉逗号 还是会出现第二次写入 即update语句后 显示0 count栏也不会变化(BUG解决 SQL语句写错了 update同一行中两项之间用逗号分隔 不能用and 之前的逗号应该不影响 但无所谓了 没有逗号也行)
#                 完成教师评价的简单前端页面以及数据库写入；想画个像储诚意那样的图;完成关于页；
#0.1.9(16.10.6)   完善参数查询(欠学生中的不良记录还没构思好)(注意：要使默认情况下显示全部的功能实现 reward等栏目必须填入值)；草创模糊查询(且仅限模糊查询名字一项，如果模糊查询多项就会通原本的默认显示全部的功能所冲突)
#                 考虑部署的问题（apache+wsgi+flask）遇到点问题
#0.2.0(16.10.7)   重要部署完成了（iis7）！！好烦有木有 装cgi python3.4 administrator pack 。。。
#                 计划施工课程公告（教师发布端，学生接收端）平时成绩显示 缺勤显示
#                 修复关于session的BUG （因为生产环境不会执行if __name__==__main__以后的代码。。）
#0.2.1(16.10.8)   完成缺勤记录在学生名册中的显示；原有的平时成绩在设定新成绩页显示（修复bug）；完成教师/学生首页的折叠菜单；
#                 载入jQuery库；实验搜索功能
#0.2.2(16.10.9)   完成历史成绩查询 学生/教师查询（教师端缺表头？不知道为何） 部署视频（但需要本地视频）
#0.2.3(16.10.10)  优化注册/登录/首页 ；分离学生和教师的首页;优化注册失败机制以及提示;完成网上学习（视频);完成意见反馈
#0.2.4(16.10.13)  完成随机学生生成
#0.2.5(16.10.14)  计划教师课程学生名册页排序 但教师评价因为学生评价的数据存储形式 无法实现
#                 创建研讨功能开发中（欠 读取表单 写入数据库 自动生成id)
#0.2.6(16.10.17)  创建研讨初步完成（欠 输入检测）;修正由于user表中id类型引发的注册失败BUG;教师/学生首页显示最新3条消息；
#                 加入按照教师评价排序功能
#0.3.0(16.10.19)  没事升个版本号 草创站内信发送 还是打算和邮件分离 完成一次性给所有班上学生发送邮件（要生成list才行。。）
#                 计划部署 查看站内信以及未读站内信
#0.4.0(16.10.29)  好久没做这个 继续完善一下 数字信号项目终于结束了！！升个版本号庆祝一下！
#                 考虑继续完善站内信功能 包括回复 消息提醒 显示所有消息等界面 修正登录后不显示消息的BUG
#0.4.1(16.10.31)  需要考虑实现一些更有技术含量的功能，而非更多的重复操作！！
#                 初步完成消息模块（欠标记删除信息 ） 考虑教师作业批改打分 试验把读取未读消息数量加到signup函数中 这样能少很多麻烦 写入session 
#记录一下 我把pylink关了（把它文件夹的名字给改了。。）
#0.4.2(16.11.1)   继续完善消息系统 完成教师作业评分前端 欠后端以及数据库 学生实装消息系统
#0.4.3(16.11.2)   实验分页 继续施工作业评分 建设两个演示账号 项目报告 放弃了教师评价排行 
#                 解决平时成绩重复显示BUG 搜索无法显示所有学生的缺陷 考虑修改学生信息（simple）
#                 分页研究暂时搁置 感觉需要一点前端知识 
#0.9.0(16.11.2)   预发布版本 将debug=true去掉   
                    

#本程序基于Python Flask网路框架==================
app=Flask(__name__)
#文件存储路径
UPLOAD_FOLDER = 'c:/flaskWebSite/file'
#允许上传的文件类型
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
'doc','docx','ppt','pptx','py'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#session的key
app.secret_key = 'lifanishuge'#need the key

#全局函数=======================================
def allowed_file(filename):
# 检测文件上传是否为允许的类型
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
def is_sign():
# 检查登陆的方法 如果登录 带上用户名以显示 附带检查未读消息
    if 'username' in session:
        #新增 会在每次调用该函数时 检查未读消息
        session['num_not_read']=mysql_model.not_read_message_num(session['username'])
        return ('true',session['username'])
    else:
        return ('false',)

#定制404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

#实验==========================================
#to do
@app.route('/bing',methods=['POST'])
def bing():
    q=request.form.get('search')
    bing_api.bing_search(q)
    return render_template('result.html')

#首页==========================================
#为什么单列出来 (部分因为我乐意)但其实确实有用（分离教师学生登录） 另外 在返回静态页面的函数中直接<>==''好像不起作用
    
@app.route('/',methods=['GET','POST'])
def home():
    #返回首页 通过登录id判断教师和学生 返回各自的首页
    if 'username' in session:
        if session['username'].startswith('1412'):
            return redirect(url_for('student_index'))
        else:
            return redirect(url_for('teacher_index'))
            #return render_template('teacher/index.html',title='欢迎教师'+session['username'],signin=is_sign())
    else:
        return render_template('home.html',title='教学管理系统',signin=is_sign()) 
    

#登陆，登出====================================
@app.route('/signin',methods=['POST','GET'])
#登陆函数 两种method分别对应登录操作和返回登录表单
def signin():
    if request.method=='POST':
        username=request.form['id']
        password=request.form['password']
                
        if mysql_model.login(username,password):
            session['username']=username
            #print('get')
            if username.startswith('1412'):
                return redirect(url_for('student_index'))
            else:
                return redirect(url_for('teacher_index'))
        return render_template('sign-form.html',title='登录',signin=is_sign(),message='登录失败')

    if request.method=='GET':
        return render_template('sign-form.html',title='登录',signin=is_sign())

@app.route('/signout',methods=['GET'])
#登出函数 考虑更好的登出方式 以及考虑SESSION有效时间的问题（目前生命周期为这个会话）
def signout():
    if request.method=='GET':
        session.pop('username', None)
        return redirect(url_for('signin',signin=is_sign()))

#注册==========================================
@app.route('/register',methods=['POST'])
#注册(还需完善：详细注册失败原因(该ID已注册；两道密码不符；)；
#考虑在注册成功返回首页后加个弹窗)
def register():
    username=request.form.get('id')
    password=request.form.get('password')
    password2=request.form.get('password2','')
    if username == '':
        return render_template('register-form.html',message='请输入注册ID',title='注册失败',signin=is_sign())   
    if password == '':
        return render_template('register-form.html',message='请输入密码',title='注册失败',signin=is_sign())
    
    if password==password2:
        session['username']=username
        
        if mysql_model.register(username,password):
            return render_template('home.html',signin=is_sign(),title='注册成功')
        else:
            return render_template('register-form.html',message='注册失败，账户已存在',title='注册失败',signin=is_sign()) 
    return render_template('register-form.html',message='请正确重复密码',title='注册失败',signin=is_sign())  

#收集意见反馈===================================
@app.route('/feedback',methods=['POST'])
def collect_advice():
    email=request.form.get('email')
    advice=request.form.get('advice')
    mysql_model.insert_advice(email,advice)
    return render_template('feedback.html',message='您的意见我们已经收到，您的意见对我们很重要，非常感谢',title='意见反馈',signin=is_sign())  

#返回静态页面===================================
@app.route('/<staic_page>',methods=['GET'])
def render_staic_page(staic_page):
    if staic_page=='find-student-form':
        return render_template('find-form.html',title='查找学生',signin=is_sign(),student=1)
    elif staic_page=='find-teacher-form':
        return render_template('find-form.html',title='查找老师',signin=is_sign(),teacher=1)
    elif staic_page=='find-course-form':
        return render_template('find-form.html',title='查找课程',signin=is_sign(),course=1)
    elif staic_page=='find-reward-form':
        return render_template('find-form.html',title='查找奖项',signin=is_sign(),reward=1)
    elif staic_page=='find-seminar-form':
        return render_template('find-form.html',title='查找研讨',signin=is_sign(),seminar=1)
    elif staic_page=='signin':
        return render_template('sign-form.html',title='登录') 
    elif staic_page=='register':
        return render_template('register-form.html',title='注册',message='',signin=is_sign())
    elif staic_page=='help':
        return render_template('help.html',tilte='帮助中心',signin=is_sign()) 
    elif staic_page=='about':
        return render_template('about.html',tilte='关于',signin=is_sign())
    elif staic_page=='feedback':
        return render_template('feedback.html',tilte='意见反馈',signin=is_sign())
    elif staic_page=='base':
        return render_template('base.html')
          
    #这样好像不起作用
    #elif staic_page=='':
     #   return render_template('home.html')

#查询所有=======================================
@app.route('/find/<find_what>',methods=['GET'])
def find_all(find_what):
#查询所有的课程 学生 老师(通过select*实现 无排序)
    if find_what=='allstudent':
        return render_template('find-result.html',
        result=mysql_model.find_all_student(),title='所有学生',student=1,signin=is_sign())
    elif find_what=='allteacher':
        return render_template('find-result.html',
        result=mysql_model.find_all_teacher(),title='所有教师',teacher=1,signin=is_sign())
    elif find_what=='allcourse':
        return render_template('find-result.html',
        result=mysql_model.find_all_course(),title='所有课程',course=1,signin=is_sign())
    elif find_what=='allreward':
        return render_template('find-result.html',
        result=mysql_model.find_all_reward(),title='所有奖项',reward=1,signin=is_sign())
    elif find_what=='allseminar':
        return render_template('find-result.html',
        result=mysql_model.find_all_seminar(),title='所有研讨',seminar=1,signin=is_sign())

#教师页操作=====================================
@app.route('/teacher/index',methods=['GET'])
def teacher_index():
    teacher_id=session['username']
    message=mysql_model.get_message(int(teacher_id))
    #message=False
    #if message is False:
     #   message='暂时没有您的消息'
    
    return render_template('teacher/index.html',title='欢迎教师'+teacher_id,
    signin=is_sign(),message=message)

@app.route('/teacher/<staic_page>',methods=['GET'])
#静态页
def render_teacher_staic_page(staic_page):
    if staic_page=='absence':
        return render_template('/teacher/student-absence.html',
        title='纪录学生缺勤',
        signin=is_sign())

@app.route('/teacher/allcourse',methods=['GET'])
def find_teacher_what():
#该函数设置考虑调整
    return find_teacher_course()
      
def find_teacher_course():
#教师查询自己所授的课程
    teacher_id=session['username']
    print(teacher_id)
    result=mysql_model.find_teacher_id(teacher_id)
    if result=='':
        result='没有你的数据'
    else:
        #print((result[0][7].split(','))[0])
        result=mysql_model.find_course_list((result[0][7].split(',')))
    return render_template('/teacher/teacher-course.html',
    result=result,title='所授课程',teacher_course='1',signin=is_sign())

@app.route('/teacher/course/<course_id>',methods=['GET','POST'])
#教师查看所授课程中的学生(进入课程页)
def find_student_in_course(course_id):
    if request.method=='GET':
        session['course_id_now']=course_id#纪录下当前操作的课程的课程后 以供后来使用 会每次刷新
        return render_template('/teacher/course-student.html',
        result=mysql_model.find_student_course(course_id),title='课程管理',
        signin=is_sign(),course_id=course_id)
    else:
        teacher_id=session['username']
        order=request.form.get('order')
        session['course_id_now']=course_id#纪录下当前操作的课程的课程后 以供后来使用 会每次刷新
        if order !='student_rate':  
            return render_template('/teacher/course-student.html',
            result=mysql_model.find_student_course_order(course_id,teacher_id,order),title='课程管理',
            signin=is_sign(),course_id=course_id)
        else:
            return render_template('/teacher/course-student.html',
            result=mysql_model.find_student_course_rate(course_id,teacher_id),title='课程管理',
            signin=is_sign(),student_rate=1)

@app.route('/teacher/student/<student_id>',methods=['GET'])
#教师管理所授课程中的学生(进入学生页)
def manage_course_student(student_id):
    return render_template('/teacher/course-student.html',
    result=mysql_model.find_student_id(student_id),title='管理课程学生',
    signin=is_sign(),student_id=student_id)

@app.route('/teacher/student/absence/<student_id>',methods=['GET','POST'])
#教师纪录单个学生缺勤(进入纪录缺勤页：第几次课缺勤)
def student_absence(student_id):
    course_id=session['course_id_now']
    absence_list=''
    absence_count=0
    if request.method=='GET':
        return render_template('/teacher/student-absence.html',
        title='纪录学生缺勤',
        signin=is_sign(),student_id=student_id,course_id=course_id)
    else:
        for x in range(1,11):
            absence=request.form.get('course_time'+str(x),None)
            if absence!=None:
                #print('course_time'+'x',absence)
                absence_list=absence_list+absence
                absence_count+=1
        print(absence_list,absence_count)
        print(mysql_model.student_absence(student_id,course_id,absence_list,absence_count))
        return render_template('/teacher/student-absence.html',
        title='纪录学生缺勤',
        signin=is_sign(),student_id=student_id,course_id=course_id,message='缺勤记录已提交，再次提交将覆盖之前的纪录')

@app.route('/teacher/student/ordinary-score/<student_id>',methods=['GET','POST'])
#教师评定单个学生平时成绩(进入学生平时成绩页)
def student_ordinary_score(student_id):
    course_id=session['course_id_now']
    if request.method=='GET':
        return render_template('/teacher/ordinary-score.html',
        title='评定学生平时成绩',result=mysql_model.find_student_id(student_id),
        signin=is_sign(),student_id=student_id,course_id=course_id)
    else:
        score=request.form.get(student_id)
        mysql_model.ordinary_score(student_id,course_id,score)
        return render_template('/teacher/ordinary-score.html',
        title='评定学生平时成绩',result=mysql_model.find_student_id(student_id),
        signin=is_sign(),student_id=student_id,course_id=course_id,message='平时成绩已提交，再次提交将覆盖之前的纪录')

@app.route('/teacher/ordinary-score/<course_id>',methods=['GET','POST'])
#教师评定课程所有学生平时成绩(进入平时成绩页)
def course_ordinary_score(course_id):
    session['course_id_now']=course_id
    if request.method=='GET':
        #进入表单
        session['course_id_now']=course_id
        return render_template('/teacher/ordinary-score.html',
        title='评定学生平时成绩',result=mysql_model.find_student_ordinary(course_id),
        signin=is_sign(),course_id=course_id)
    else:
        #提交成绩
        score=request.form.to_dict()
        for x in score:
            print(x,score[x])
            mysql_model.ordinary_score(x,course_id,score[x])
        return render_template('/teacher/ordinary-score.html',
        title='评定学生平时成绩',result=mysql_model.find_student_ordinary(course_id),
        signin=is_sign(),course_id=course_id,message='平时成绩已提交，再次提交将覆盖之前的纪录')

@app.route('/teacher/homework/score/<course_id>',methods=['POST'])
#教师给作业打分
def homework_score(course_id):
    score=request.form.to_dict()
    for x in score:
        #print(x,score[x])
        mysql_model.homework_score(x,course_id,score[x])
    return redirect(url_for('teacher_correct_work',course_id=course_id,message='作业成绩已提交，再次提交将覆盖之前的纪录'))

@app.route('/teacher/student/score/<student_id>',methods=['GET'])
#教师查看指定学生成绩历史成绩
def student_history_score(student_id):
    
    result=mysql_model.find_history_score(student_id)
    return render_template('/student/student-result.html',
    result=result,student_score=1,title='查看历史成绩',signin=is_sign())

@app.route('/teacher/seminar/<teacher_id>',methods=['GET','POST'])
#教师创建研讨
def teacher_create_seminar(teacher_id):
    if request.method=='GET':
        return render_template('/teacher/seminar.html',teacher_id=teacher_id,
        title='创建研讨',signin=is_sign())
    else:
        teacher_id=session['username']
        seminar_name=request.form.get('seminar_name')
        seminar_time=request.form.get('seminar_time')
        seminar_location=request.form.get('seminar_location')
        mysql_model.insert_seminar(seminar_name,teacher_id,seminar_location,seminar_time)
        return render_template('/teacher/seminar.html',teacher_id=teacher_id,
        title='创建研讨',signin=is_sign(),message='创建完成')

@app.route('/teacher/course-work/<course_id>',methods=['GET'])
#教师查看学生作业(进入课程作业页)
def teacher_correct_work(course_id,message=''):
    find_work=True
    all_work={}
    session['course_id_now']=course_id
    result=mysql_model.find_student_course(course_id)
    dir_course_path=os.path.join(app.config['UPLOAD_FOLDER'],session['course_id_now'])
    if os.path.isdir(dir_course_path):
        for student in result:
            student_id=student[0]
            dir_student_path=os.path.join(app.config['UPLOAD_FOLDER'],session['course_id_now'],str(student_id))
            if os.path.isdir(dir_student_path):
                all_work[student_id]=[x for x in os.listdir(dir_student_path)]
            else:
                all_work[student_id]=['尚未上传']                     

    else:
        find_work=False
    #print(find_work,all_work)
    return render_template('/teacher/course-work.html',
    title='批改作业',
    signin=is_sign(),result=result,course_id=course_id,find_work=find_work,all_work=all_work,message=message)



@app.route('/teacher/course-work/open/<student_id>/<filename>',methods=['GET'])
#打开对应的文件
def open_file(student_id,filename):
    
    print(student_id,filename)
    print(session['course_id_now'])
   

    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],session['course_id_now'],student_id),filename)
#
#'d:/test/1001/14120001'

#学生页操作============================================
@app.route('/student/index',methods=['GET'])
def student_index():
    student_id=session['username']
    message=mysql_model.get_message(int(student_id))
    return render_template('student/index.html',title='欢迎同学'+session['username'],
    signin=is_sign(),message=message)

@app.route('/student/allcourse',methods=['GET'])
#学生查看自己所有课程
def student_all_course():
    student_id=session['username']
    print(student_id)
    result=mysql_model.find_student_id(student_id)
    if result=='':
        result='没有你的数据'
    #print((result[0][0].split(','))[0])
    else:
        result=mysql_model.find_course_list((result[0][8].split(',')))
   
    return render_template('/student/student-result.html',
    result=result,course=1,title='所选课程',signin=is_sign())

@app.route('/student/course-teacher/<course_id>',methods=['GET'])
#学生查看上课的老师(进入教师页)
def find_teacher_in_course(course_id):
    session['course_id_now']=course_id
    result=mysql_model.find_teacher_course(course_id)
    return render_template('/student/student-result.html',
    result=result,teacher=1,title='查看教师',signin=is_sign())

@app.route('/student/rate/<teacher_id>',methods=['GET','POST'])
#学生评价教师
def student_rate_teacher(teacher_id):
    student_id=session['username']
    course_id=session['course_id_now']
    rate=''
    score=0
    if request.method=='GET':
        return render_template('/student/teacher-rate.html',
        title='评价教师',signin=is_sign(),teacher_id=teacher_id)
    else:
        for x in range(1,6):
            rate+=request.form.get(str(x),None)
            score+=int(request.form.get(str(x),None))
        print(rate,score)
        mysql_model.rate_teacher(student_id,teacher_id,course_id,rate,score)
        return render_template('/student/teacher-rate.html',
        title='评价教师',signin=is_sign(),teacher_id=teacher_id,message='教师评价已提交，再次提交将覆盖之前的纪录')

@app.route('/student/online-learn',methods=['POST','GET'])
#学生在线学习
def student_online_learn():
    if request.method=='GET':
        return render_template('/student/online-learn.html',
        title='在线学习',signin=is_sign(),message='')

@app.route('/student/score',methods=['GET'])
#学生查看历史成绩(进入学生结果页)
def find_history_score():
    student_id=session['username']
    result=mysql_model.find_history_score(student_id)
    return render_template('/student/student-result.html',
    result=result,score=1,title='查看历史成绩',signin=is_sign())

@app.route('/student/course-work/<course_id>',methods=['POST','GET'])
#学生上传对应课程的作业(全力施工中)
def student_homework(course_id):
    session['course_id_now']=course_id#纪录下当前操作的课程的课程后 以供后来使用 会每次刷新
    if request.method=='GET':
        return render_template('/student/student-homework.html'
        ,course_id=course_id,title='上传作业',signin=is_sign())
    if request.method=='POST':
        file = request.files['file']
        #print(allowed_file(file.filename))
        #文件类型规定
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #如果首次上传则需要先新建课程/学号；两层文件夹
            dir_course_path=os.path.join(app.config['UPLOAD_FOLDER'],session['course_id_now'])
            dir_student_path=os.path.join(app.config['UPLOAD_FOLDER'],session['course_id_now'],session['username'])
            if not os.path.isdir(dir_course_path):
                os.mkdir(dir_course_path)
            if not os.path.isdir(dir_student_path):
                os.mkdir(dir_student_path)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],session['course_id_now'],session['username'],filename))
            return render_template('/student/student-homework.html'
            ,course_id=course_id,title='上传成功',signin=is_sign())
        return render_template('/student/student-homework.html'
        ,course_id=course_id,title='上传失败',signin=is_sign())

#精确参数查找=========================================
@app.route('/find/<find_what>',methods=['POST'])
def find_what(find_what):
   
    if find_what=='student':
        return find_student()
    elif find_what=='course':
        return find_course()
    elif find_what=='teacher':
        return find_teacher()
    elif find_what=='reward':
        return find_reward()
    elif find_what=='seminar':
        return find_seminar()
    

def find_student():
    #通过学生参数数据库查找函数
    item=['student_id','student_name','student_gpa_max','student_gpa_min',
    'order','up_or_down','is_dishonour','student_course','student_grade',
    'student_reward','student_seminar','student_grade','student_major']
    #页面表单输入项 学生学号，学生姓名等，表单若不填默认为''
    cond={x:request.form.get(x) for x in item}
    #通过生成器生成学生查找参数字典

    result=mysql_model.find_some_student(cond)
    #通过字典参数传递给数据库查找函数
    print(result)#测试返回结果
    if result=='':
        result='没有符合的同学'
    #没有符合条件的学生
    return render_template('find-result.html',
    result=result,title='found students',student='1',signin=is_sign())
    #返回在静态页面上动态生成的学生搜索结果，设定标题，结果类型为学生，以及注册信息

def find_course():
    item=['course_id','course_name','course_time','course_location']

    cond={x:request.form.get(x) for x in item}

    result=mysql_model.find_some_course(cond)
    print(result)
    if result=='':
        result='没有符合的课程'
    return  render_template('find-result.html',
    result=result,title='found courses',course='1',signin=is_sign())

def find_teacher():
    item=['teacher_id','teacher_name','teacher_seminar','teacher_college',
    'order','up_or_down','teacher_course','teacher_college']
    
    cond={x:request.form.get(x) for x in item}
    #表单若不填为''
    
    result=mysql_model.find_some_teacher(cond)
    print(result)
    if result=='':
        result='没有符合的教师'
    return render_template('find-result.html',
    result=result,title='found teachers',teacher='1',signin=is_sign())

def find_reward():
    item=['reward_id','reward_name','reward_student_id']

    cond={x:request.form.get(x) for x in item}

    result=mysql_model.find_some_reward(cond)
    print(result)
    if result=='':
        result='没有符合的奖项'
    return  render_template('find-result.html',
    result=result,title='查找奖项',reward=1,signin=is_sign())

def find_seminar():
    item=['seminar_id','seminar_name','seminar_student_id','seminar_teacher_id']

    cond={x:request.form.get(x) for x in item}

    result=mysql_model.find_some_seminar(cond)
    print(result)
    if result=='':
        result='没有符合的研讨项目'
    return  render_template('find-result.html',
    result=result,title='查找研讨',seminar=1,signin=is_sign())

def find_reward():
    item=['reward_id','reward_name','reward_student_id']

    cond={x:request.form.get(x) for x in item}

    result=mysql_model.find_some_reward(cond)
    print(result)
    if result=='':
        result='没有符合的奖项'
    return  render_template('find-result.html',
    result=result,title='查找研讨',reward=1,signin=is_sign())

#模糊查询===============================================
@app.route('/find/regex/<find_what>',methods=['POST'])
def find_regex_what(find_what):
    if find_what=='student':
        return find_student_regex()
    elif find_what=='teacher':
        return find_teacher_regex()
    elif find_what=='course':
        return find_course_regex()
    elif find_what=='seminar':
        return find_seminar_regex()
    elif find_what=='reward':
        return find_reward_regex()

def find_student_regex():
    item=['student_id','student_name','student_gpa_max','student_gpa_min',
    'order','up_or_down','is_dishonour','student_course','student_grade',
    'student_reward','student_seminar','student_grade','student_major']
    cond={x:request.form.get(x) for x in item}
    result=mysql_model.find_some_student(cond,True)
    print(result)
    if result=='':
        result='没有符合的同学'
    return render_template('find-result.html',
    result=result,title='found students',student='1',signin=is_sign())

def find_course_regex():
    item=['course_id','course_name','course_time','course_location']

    cond={x:request.form.get(x) for x in item}

    result=mysql_model.find_some_course(cond,True)
    print(result)
    if result=='':
        result='没有符合的课程'
    return  render_template('find-result.html',
    result=result,title='found courses',course='1',signin=is_sign())

def find_teacher_regex():
    item=['teacher_id','teacher_name','teacher_seminar','teacher_college'
    ,'order','up_or_down','teacher_course','teacher_college']
    
    cond={x:request.form.get(x) for x in item}
    #表单若不填为''
    
    result=mysql_model.find_some_teacher(cond,True)
    print(result)
    if result=='':
        result='没有符合的教师'
    return render_template('find-result.html',
    result=result,title='found teachers',teacher='1',signin=is_sign())

def find_seminar_regex():
    item=['seminar_id','seminar_name','seminar_student_id','seminar_teacher_id']

    cond={x:request.form.get(x) for x in item}

    result=mysql_model.find_some_seminar(cond,True)
    print(result)
    if result=='':
        result='没有符合的研讨项目'
    return  render_template('find-result.html',
    result=result,title='查找研讨',seminar=1,signin=is_sign())

def find_reward_regex():
    item=['reward_id','reward_name','reward_student_id']

    cond={x:request.form.get(x) for x in item}

    result=mysql_model.find_some_reward(cond,True)
    print(result)
    if result=='':
        result='没有符合的奖项'
    return  render_template('find-result.html',
    result=result,title='查找研讨',reward=1,signin=is_sign())
#站内信部分=============================================
@app.route('/allmessage',methods=['GET'])
def check_all_message():
    #查看所有消息，并将所有未读消息转为已读

    receiver_id=session['username']
    result=mysql_model.get_all_message(receiver_id)
    mysql_model.set_message_read(receiver_id)
    return render_template('all-message.html',title='我的消息',signin=is_sign(),result=result)

@app.route('/allmessage/<action>',methods=['GET'])
def message_action(action):
    #操作所有消息
    receiver_id=session['username']
    if action=='read-all':
        mysql_model.set_message_read(receiver_id)
        result=mysql_model.get_all_message(receiver_id)
        message='已将所有消息设为已读'
        return render_template('all-message.html',title='我的消息',
        signin=is_sign(),message=message,result=result)
    elif action=='not-read-all':
        mysql_model.set_message_not_read(receiver_id) 
        result=mysql_model.get_all_message(receiver_id)
        message='已将所有消息设为未读'
        return render_template('all-message.html',title='我的消息',
        signin=is_sign(),message=message,result=result)
    elif action=='delete-all':
        mysql_model.delete_all_message(receiver_id)
        result=mysql_model.get_all_message(receiver_id)
        message='已将所有消息删除，但可通过联系网站恢复'
        return render_template('all-message.html',title='我的消息',
        signin=is_sign(),message=message,result=result)
        

@app.route('/message',methods=['POST','GET'])
def send_message():
    #发送站内信页面
    if request.method=='POST':
        sender=session['username']
        to=request.form['to']
        title=request.form['title']
        text=request.form['text']
        mysql_model.insert_message(to,sender,text)
        return render_template('message-form.html',title='发送站内信',signin=is_sign())
    else:
        return render_template('message-form.html',title='发送站内信',signin=is_sign())

@app.route('/message/<receiver_id>',methods=['GET'])
def send_message_2sb(receiver_id):
    #发送站内信给某人
    return render_template('message-form.html',title='发送站内信',
        signin=is_sign(),receiver_id=receiver_id)

@app.route('/message/course/<course_id>',methods=['GET','POST'])
def send_message_2_course(course_id):
    #发送站内信给某班级的全部同学
    sender_id=session['username']
    if request.method=='POST':
        message=request.form['text']
        mysql_model.all_course_message(course_id,sender_id,message)
        return render_template('/teacher/message-course-form.html',title='班级通知已发送',
            signin=is_sign(),message='班级通知已发送')
    else:
        return render_template('/teacher/message-course-form.html',title='班级通知',
            signin=is_sign(),course_id=course_id)
#邮件部分===============================================
@app.route('/email')
def email():
    receiver=request.args.get('receiver')
    signin=request.args.get('signin')
    return render_template('email-form.html',title='发送邮件',signin=is_sign())

@app.route('/contact-allstudent/<course_id>')
#联系课程中所有学生
def contact_allstudent(course_id):
    receiver_email=mysql_model.get_course_all_email(course_id)
    print(receiver)
    return render_template('email-form.html',title='发送邮件',
    signin=is_sign(),receiver_email=receiver_email,receiver_name='全体同学')

@app.route('/contact-student/<student_id>')
#联系学生
def contact_student(student_id):
    receiver=mysql_model.find_student_id(student_id)
    print(receiver)
    return render_template('email-form.html',title='发送邮件',
    signin=is_sign(),receiver_email=receiver[0][4],receiver_name=receiver[0][1])

@app.route('/contact-teacher/<teacher_id>')
#联系教师(待施工 考虑自动加上发送邮件的学生姓名ps：其实就是session中的学号)（已取消，不重要）
def contact_teacher(teacher_id):
    receiver=mysql_model.find_teacher_id(teacher_id)
    print(receiver)
    return render_template('email-form.html',title='发送邮件',
    signin=is_sign(),receiver_email=receiver[0][3],receiver_name=receiver[0][1])
    #return redirect(url_for('email',signin=is_sign(),receiver=receiver))

@app.route('/send-email',methods=['POST'])
def sending_email():
#根据勾选的情况 发送给个人/多人（取消）
    return send_email2person()
  
def send_email2person():
#发送email给指定的收件人
    to=email_regex.get_email(request.form['to'])
    title=request.form['title']
    text=request.form['text']
    if (to!=None) and (to!=''):
        try:
            send_email.sendemail(to,title,text)
            return render_template('email-form.html',message='sent',signin=is_sign())
        
        except :
            return render_template('email-form.html',message='failed',signin=is_sign()) 
    else:
        return render_template('email-form.html',message='bad email address',signin=is_sign())
        
#def send_email2all():
#发送email给多人(施工/考虑中)(已取消)
#    return render_template('email-form.html',message='Working on it!',signin=is_sign())


#主函数======================================
if __name__=='__main__':
    app.run()
