import random,mysql.connector


name_boy='伟 刚 勇 毅 俊 峰 强 军 平 保 东 文 辉 力 明 永 健 世 广 志 义 兴 良 海 山 仁 波 宁 贵 福 生 龙 元 全 国 胜 学 祥 才 发 武 新 利 清 飞 彬 富 顺 信 子 杰 涛 昌 成 康 星 光 天 达 安 岩 中 茂 进 林 有 坚 和 彪 博 诚 先 敬 震 振 壮 会 思 群 豪 心 邦 承 乐 绍 功 松 善 厚 庆 磊 民 友 裕 河 哲 江 超 浩 亮 政 谦 亨 奇 固 之 轮 翰 朗 伯 宏 言 若 鸣 朋 斌 梁 栋 维 启 克 伦 翔 旭 鹏 泽 晨 辰 士 以 建 家 致 树 炎 德 行 时 泰 盛'

name_girl='筠 柔 竹 霭 凝 晓 欢 霄 枫 芸 菲 寒 伊 亚 宜 可 姬 舒 影 荔 枝 思 丽 秀 娟 英 华 慧 巧 美 娜 静 淑 惠 珠 翠 雅 芝 玉 萍 红 娥 玲 芬 芳 燕 彩 春 菊 勤 珍 贞 莉 兰 凤 洁 梅 琳 素 云 莲 真 环 雪 荣 爱 妹 霞 香 月 莺 媛  艳 瑞 凡 佳 嘉 琼 桂 娣 叶 璧 璐 娅 琦 晶 妍 茜 秋 珊 莎 锦 黛 青 倩 婷 姣 婉 娴 瑾 颖 露 瑶 怡 婵 雁 蓓 纨 仪 荷 丹 蓉 眉 君 琴 蕊 薇 菁 梦 岚 苑 婕 馨 瑗 琰 韵 融 园 艺 咏 卿 聪 澜 纯 毓 悦 昭 冰 爽 琬 茗 羽 希 宁 欣 飘 育 滢 馥'


surname=['赵','钱','孙','李','周','吴','郑','王','冯',
'陈','丁','廖','邓','毛','刘','朱','宋','齐','梁','赵',
'杨','黄','林','顾','姚','徐','许','武','章','张','肖',
'马','牛','牟','杜','楚','曾','秦','郜','蒿','郝','冯']

name_list_boy=name_boy.split(' ')
name_list_girl=name_girl.split(' ')
list_name=[]

def create_phonenumber():
    pnum='13'
    pnum+=str(random.randint(000000000,999999999))
    #print(pnum)
    return pnum

def create_email():
    email_server=['@qq.com','@163.com']
    if random.randint(0,1)==0:
        qq=str(random.randint(300000000,1300000000))
        return qq+'@qq.com'
    else:
        return creat_phonenumber()+'@163.com'

def create_gpa():
    return str(random.randint(0,3))+'.'+str(random.randint(000,999))

def create_course():
    course_count=random.randint(1,4)
    if course_count==1:
        return str(random.randint(1001,1004))
    elif course_count==2:
        return str(random.randint(1001,1004))+','+str(random.randint(1001,1004))
    elif course_count==3:
        return str(random.randint(1001,1004))+','+str(random.randint(1001,1004))+','+str(random.randint(1001,1004))
    else:
        return str(random.randint(1001,1004))+','+str(random.randint(1001,1004))+','+str(random.randint(1001,1004))+','+str(random.randint(1001,1004))

def creat_major():
    rand=random.randint(1,15)
    if rand<12:
        return '通信工程'
    elif rand<14:
        return '电子信息工程'
    else:
        return '生物医学工程'

def create_name(): 
    girl_boy=random.randint(0,1)
    one_two=random.randint(0,2)
    if girl_boy==1:
        if one_two!=0:#(25%单名)
            student_name=surname[random.randint(0,41)]+name_list_boy[random.randint(1,130)]+name_list_boy[random.randint(1,130)]
        else:
            student_name=surname[random.randint(0,41)]+name_list_boy[random.randint(1,130)]
    else:
        if one_two!=0:
            student_name=surname[random.randint(0,41)]+name_list_girl[random.randint(1,140)]+name_list_girl[random.randint(1,140)]
        else:
            student_name=surname[random.randint(0,41)]+name_list_girl[random.randint(1,140)]
    #print(student_name)

    return student_name       
def create_student(start,end):
    grade='3'
    no='None'
    for x in range(start,end):
        conn = mysql.connector.connect(host='115.28.221.228',user='lf',
        password='159753',database='intelligent_teaching_system')
        cursor = conn.cursor()
        sql='insert into student values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        result=cursor.execute(sql,(x,create_name(),grade,create_major(),create_email(),create_phonenumber(),create_gpa(),no,create_course(),no,no))
        cursor.close()
        conn.commit()
        conn.close()
        #print(x)
        #print(create_email())

if __name__=='__main__':

    
