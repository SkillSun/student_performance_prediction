# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 10:32:31 2017

@author: Skill Sun
"""
# import xlrd
import xlwt
import datetime
import mysql.connector
from mysql.connector import errorcode


class Banji:  # 班级类
    def __init__(self, id):
        self.id = id  # 班级id(外部id，非数据库id)
        self.semester = ""  # 学期名称
        self.subject = ""  # 课程名称
        self.banji_name = ""  # 班级名称
        self.teacher = ""  # 教师名称
        self.students = []  # 学生和学号
        self.homeworks = []  # 作业id，名称，开始时间，结束时间，满分值
        self.homeworkid_to_col = {}  # 作业id到Excel表格列号的映射
        self.homework_results = []  # 作业成绩和时间
        self.final_score = []  # 期末总评

    def show(self):
        print("学期：  " + self.semester)
        print("课程名：" + self.subject)
        print("班级名：" + self.banji_name)
        print("教师名：" + self.teacher)
        print("学生列表：")
        print(self.students)
        print("作业列表：")
        print(self.homeworks)
        print("作业结果：")
        print(self.homework_results)
        print("最终得分：")
        print(self.final_score)


# TODO: 服务器连接设置
config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'database': 'db_student',
    'raise_on_warnings': True
}

# 尝试连接并在异常时提示错误
try:
    cnx = mysql.connector.connect(**config)  # cnx 为连接数据库的接口
    cnx2 = mysql.connector.connect(**config)  # cnx2 也是连接数据库的接口
    cnx3 = mysql.connector.connect(**config)  # cnx3 还是连接数据库的接口
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or passsword")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Connection Successed.")

# 初始化一大堆文件端口
book = xlwt.Workbook()  # 用于存放数据的Excel表格
excel_row = 0  # 写入数据的行号
excel_col = 0  # 写入数据的列号
cursor = cnx.cursor()
cursor2 = cnx2.cursor()
cursor3 = cnx3.cursor()
query = ""
query2 = ""
query3 = ""
total_banji = []  # 用于存放所有班级的列表

query = ("SELECT id, name, start_time, courser_id, teacher_id FROM work_banji")
cursor.execute(query)
i = 0
for (work_banji_id, name, start_time, courser_id, teacher_id) in cursor:
    stu_sheet = book.add_sheet(name + '(id=' + str(work_banji_id) + ')', True)  # 每个班级一个工作表
    banji = Banji(i)  # 在内存中新建班级
    # 第零步：写入班级名称
    banji.banji_name = name
    stu_sheet.write(2, 0, "班级名称")
    stu_sheet.write(2, 1, name)
    # 第零步+1：写入学期名称
    stu_sheet.write(0, 0, "学期")
    if (start_time < datetime.datetime(2016, 12, 31, 0, 0, 0)):
        banji.semester = "2016-2017学年第一学期"
        stu_sheet.write(0, 1, "2016-2017学年第一学期")
    else:
        banji.semester = "2016-2017学年第二学期"
        stu_sheet.write(0, 1, "2016-2017学年第二学期")
    # 第一步：写入课程名称
    query2 = ("SELECT id, name FROM class_name WHERE id = '%s'" % courser_id)
    cursor2.execute(query2)
    for (class_name_id, name) in cursor2:
        banji.subject = name
        stu_sheet.write(1, 0, "课程名称")
        stu_sheet.write(1, 1, name)
    # 第二步：写入教师名称
    query2 = ("SELECT id, id_num, username FROM auth_system_myuser WHERE id = '%s'" % teacher_id)
    cursor2.execute(query2)
    for (auth_system_myuser_id, id_num, username) in cursor2:
        banji.teacher = username
        stu_sheet.write(3, 0, "教师姓名")
        stu_sheet.write(3, 1, username)

    """ 
    到此为止一切正常
    Fine up here.
    """
    # 第三步：得到班内学生id
    query2 = ("SELECT myuser_id FROM work_banji_students WHERE banji_id = '%s'" % work_banji_id)
    cursor2.execute(query2)
    stu_sheet.write(5, 0, "学生学号")
    stu_sheet.write(5, 1, "学生姓名")
    excel_row = 6
    for (myuser_id) in cursor2:
        # 第四步：得到学生信息
        query3 = ("SELECT id, id_num, username FROM auth_system_myuser WHERE id = '%s'" % myuser_id)
        cursor3.execute(query3)
        for (auth_system_myuser_id, id_num, username) in cursor3:
            student = [auth_system_myuser_id, id_num, username]
            banji.students.append(student)
            stu_sheet.write(excel_row, 0, id_num)
            stu_sheet.write(excel_row, 1, username)
            excel_row = excel_row + 1
    """
    Debugged.
    """
    # 第五步：得到班级作业Id
    query2 = ("SELECT myhomework_id FROM work_myhomework_banji WHERE banji_id = '%s'" % work_banji_id)
    cursor2.execute(query2)
    excel_col = 2
    stu_sheet.write(4, 0, "作业名称")
    for (myhomework_id) in cursor2:
        # 第六步：得到班级作业信息
        query3 = (
        "SELECT id, name, start_time, end_time, total_score FROM work_myhomework WHERE id = '%s'" % myhomework_id)
        cursor3.execute(query3)
        for (work_myhomework_id, name, start_time, end_time, total_score) in cursor3:
            zuoye = [work_myhomework_id, name, start_time, end_time, total_score]
            banji.homeworks.append(zuoye)
            banji.homeworkid_to_col[work_myhomework_id] = excel_col
            stu_sheet.write(4, excel_col, name)
            excel_col = excel_col + 2
    """
    Debugged.
    """
    # 第七 + 第八步：得到班级内每个学生的每次作业信息
    excel_row = 6
    for (auth_system_myuser_id, id_num, username) in banji.students:
        for (work_myhomework_id, name, start_time, end_time, total_score) in banji.homeworks:
            query2 = (
            "SELECT id, score, create_time FROM work_homeworkanswer WHERE creator_id = '%s' AND homework_id = '%s'" % (
            auth_system_myuser_id, work_myhomework_id))
            cursor2.execute(query2)
            for (work_homeworkanswer_id, score, create_time) in cursor2:
                result = [work_homeworkanswer_id, score, create_time]
                banji.homework_results.append(result)
                stu_sheet.write(excel_row, banji.homeworkid_to_col[work_myhomework_id], score)
                stu_sheet.write(excel_row, banji.homeworkid_to_col[work_myhomework_id] + 1, str(create_time))
        excel_row = excel_row + 1
    banji.show()
    total_banji.append(banji)
    i = i + 1
    book.save('C:\\Users\\admin\\Desktop\\test.xls')
    print("Pause Here!")

# 关闭所有端口
cursor.close()
cursor2.close()
cursor3.close()
cnx.close()
cnx2.close()
cnx3.close()
book.save('C:\\Users\\admin\\Desktop\\test.xls')

print("Finished\n")
