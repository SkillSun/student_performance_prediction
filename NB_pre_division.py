# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 09:46:13 2017

@author: Skill Sun

为了将要进行的贝叶斯分类预先处理数据
将学生的学习成绩，作业提交时间和作业成绩分层
以文本文档形式输出到文件夹中

"""

import xlrd
import time
from NB_options import Options

# 根据所读取的数据情况进行分类
if Options.IS_ONLY_SUMMARY:
    BEGIN_COL = 3
else:
    BEGIN_COL = 5
BEGIN_ROW = 4


# 定义计算时间差函数
def get_time_leap(pre_str, aft_str):
    if aft_str == 'NULL':
        return 0
    pre_time = time.strptime(pre_str, '%Y-%m-%d %H:%M:%S')
    aft_time = time.strptime(aft_str, '%Y-%m-%d %H:%M:%S')
    pre_sec = time.mktime(pre_time)
    aft_sec = time.mktime(aft_time)
    return pre_sec - aft_sec


# 定义分区函数
def get_mark(percentage, percentage_list):
    result = 0
    for top in percentage_list:
        result = top[1]
        if percentage > top[0]:
            break
    return result


# 定义列表到文件函数
def write_list(in_list, file_cursor):
    in_string = ""
    for elem in in_list:
        in_string = in_string + str(elem) + ' '
    # print(in_string)
    file_cursor.write(in_string + '\n')


# 定义文件函数
def NB_pre_division(
        pre_in_file_route=Options.PRE_IN_FILE_ROUTE,
        pre_out_file_directory=Options.PRE_OUT_FILE_DIRECTORY,
        is_only_summary=Options.IS_ONLY_SUMMARY,
        score_percentage_list=Options.SCORE_PERCENTAGE_LIST,
        time_percentage_list=Options.TIME_PERCENTAGE_LIST
        ):
    # 打开资源文件
    data_file = xlrd.open_workbook(pre_in_file_route)
    # 读取表单上的内容
    for sheet_index in range(data_file.nsheets):
        # 打开目标文件
        sheet = data_file.sheet_by_index(sheet_index)
        output_file = open(pre_out_file_directory + str(sheet_index) + '.txt', 'w+')

        # 标题行处理
        end_row = sheet.nrows
        end_col = sheet.ncols

        # 读取标题行数据
        title_row = sheet.row_values(BEGIN_ROW)
        # 标题行整理并输出
        title_row[0] = "学号"
        title_row[1] = "姓名"
        if is_only_summary:
            title_row[2] = "总评成绩"
            output_row = title_row[0:3]
            for elem_index in range(3, len(title_row), 2):
                output_row.append(title_row[elem_index])
                output_row.append(title_row[elem_index] + '时间')
        else:
            title_row[2] = "平时成绩"
            title_row[3] = "期末成绩"
            title_row[4] = "总评成绩"
            output_row = title_row[0:5]
            for elem_index in range(5, len(title_row), 2):
                output_row.append(title_row[elem_index])
                output_row.append(title_row[elem_index] + '时间')
        write_list(output_row, output_file)

        # 读取内容行数据
        cur_row = 6
        students_data = []
        work_time = ["" for i in range(len(title_row))]
        while cur_row < end_row:
            # 读取一行数据
            data = sheet.row_values(cur_row)
            # 剔除错误(没有总评)的数据
            if data[BEGIN_COL - 1] == "":
                cur_row = cur_row + 1
                continue
            else:
                # 将所有未交作业改为0,记录所有已交的作业的最早和最迟提交时间
                for cur_col in range(BEGIN_COL, end_col, 2):
                    if data[cur_col] == "":
                        data[cur_col] = 0
                        data[cur_col + 1] = "NULL"
                    else:
                        # 记录时间,cur_col为最早，cur_col + 1为最迟
                        if work_time[cur_col] == "" or work_time[cur_col] > data[cur_col + 1]:
                            work_time[cur_col] = data[cur_col + 1]
                        if work_time[cur_col + 1] == "" or work_time[cur_col + 1] < data[cur_col + 1]:
                            work_time[cur_col + 1] = data[cur_col + 1]
            students_data.append(data)
            cur_row = cur_row + 1

        # 内容行整理并输出
        for data in students_data:
            rank = data
            for cur_col in range(2, BEGIN_COL):
                rank[cur_col] = get_mark(rank[cur_col], score_percentage_list)
            # 处理时间的提交阶段为百分比(时间得分)
            # (截止-提交)/(截止-开始)=提交排名百分比，值越高交得越早
            # 字符串转换为时间
            for cur_col in range(BEGIN_COL, end_col, 2):
                rank[cur_col] = get_mark(rank[cur_col], score_percentage_list)
                time_sec = get_time_leap(work_time[cur_col + 1], rank[cur_col + 1])
                time_sum = get_time_leap(work_time[cur_col + 1], work_time[cur_col])
                time_score = time_sec / time_sum * 100
                rank[cur_col + 1] = get_mark(time_score, time_percentage_list)
            write_list(rank, output_file)
        output_file.close()


# DEBUG: NB_pre_division()
