# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 22:39:31 2017

@author: Skill Sun

循环整个文件,判断当前分组的可靠性
"""
from NB_pre_division import NB_pre_division
from NB_division import NBDivision
from NB_options import Options
import xlwt


def reliability_judge():
    # 循环两个用于分区的列表
    book = xlwt.Workbook()
    test_sheet = book.add_sheet("test", True)
    xl_row = 0
    out_list = []
    # 有效成绩范围：20~98, 即range(20, 99), 成绩(三个成绩总和的)的最高分和最低分
    # 有效时间范围：35~99, 即range(35, 100)
    for time in range(1, 99):
        for score in range(20, 100):
            time_percentage_list = [[time, '早'], [0, '晚']]
            score_percentage_list = [[score, '及格'], [0, '不及格']]
            # 预处理文件
            NB_pre_division(
                    pre_in_file_route=Options.PRE_IN_FILE_ROUTE,
                    pre_out_file_directory=Options.PRE_OUT_FILE_DIRECTORY,
                    is_only_summary=Options.IS_ONLY_SUMMARY,
                    score_percentage_list=score_percentage_list,
                    time_percentage_list=time_percentage_list
                    )
            # 读取第i行的数据
            chance = NBDivision(
                    file_str=Options.PRE_OUT_FILE_DIRECTORY,
                    pre_list=Options.pre_index_list,
                    aft_list=Options.aft_index_list
                    )
            # print('time = ', time, ', score = ', score)
            # print(chance.get_pro(Options.query_string))
            out_tuple = chance.get_pro(Options.query_string)
            out_list = [time, score] + out_tuple[0]+out_tuple[1]
            for elem_index in range(len(out_list)):
                test_sheet.write(xl_row, elem_index, out_list[elem_index])
            xl_row = xl_row + 1
        book.save('C:\\Users\\admin\\Desktop\\test4.xls')
        print(out_list)


# 除了第i行的内容用于训练分类器
# 用第i行的数据作为query_str来进行判断
# 记录总判断次数和正确判断次数
# 输出结果到excel表格中
reliability_judge()
