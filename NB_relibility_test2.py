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
    test_sheet1 = book.add_sheet("test1", True)
    test_sheet2 = book.add_sheet("test2", True)
    test_sheet3 = book.add_sheet("test3", True)
    test_sheet4 = book.add_sheet("test4", True)
    test_sheet5 = book.add_sheet("test5", True)
    test_sheet6 = book.add_sheet("test6", True)
    test_sheet7 = book.add_sheet("test7", True)

    sheet1_row = 0
    sheet2_row = 0
    sheet3_row = 0
    sheet4_row = 0
    sheet5_row = 0
    sheet6_row = 0
    sheet7_row = 0

    out_list = []
    # 有效成绩范围：20~98, 即range(20, 99), 成绩(三个成绩总和的)的最高分和最低分
    # 有效时间范围：35~99, 即range(35, 100)
    for time in range(1, 100):
        for score in range(20, 44):
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
            out_tuple = chance.get_pro(Options.query_string)
            out_list = [time, score] + out_tuple[0]+out_tuple[1]
            for elem_index in range(len(out_list)):
                test_sheet1.write(sheet1_row, elem_index, out_list[elem_index])
            sheet1_row = sheet1_row + 1
        book.save('C:\\Users\\admin\\Desktop\\test5.xls')
        print(out_list)

        for score in range(44, 60):
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
            out_tuple = chance.get_pro(Options.query_string)
            out_list = [time, score] + out_tuple[0]+out_tuple[1]
            for elem_index in range(len(out_list)):
                test_sheet2.write(sheet2_row, elem_index, out_list[elem_index])
            sheet2_row = sheet2_row + 1
        book.save('C:\\Users\\admin\\Desktop\\test5.xls')
        print(out_list)

        for score in range(60, 73):
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
            out_tuple = chance.get_pro(Options.query_string)
            out_list = [time, score] + out_tuple[0]+out_tuple[1]
            for elem_index in range(len(out_list)):
                test_sheet3.write(sheet3_row, elem_index, out_list[elem_index])
            sheet3_row = sheet3_row + 1
        book.save('C:\\Users\\admin\\Desktop\\test5.xls')
        print(out_list)

        for score in range(73, 83):
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
            out_tuple = chance.get_pro(Options.query_string)
            out_list = [time, score] + out_tuple[0]+out_tuple[1]
            for elem_index in range(len(out_list)):
                test_sheet4.write(sheet4_row, elem_index, out_list[elem_index])
            sheet4_row = sheet4_row + 1
        book.save('C:\\Users\\admin\\Desktop\\test5.xls')
        print(out_list)

        for score in range(83, 97):
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
            out_tuple = chance.get_pro(Options.query_string)
            out_list = [time, score] + out_tuple[0]+out_tuple[1]
            for elem_index in range(len(out_list)):
                test_sheet5.write(sheet5_row, elem_index, out_list[elem_index])
            sheet5_row = sheet5_row + 1
        book.save('C:\\Users\\admin\\Desktop\\test5.xls')
        print(out_list)

        for score in range(97, 98):
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
            out_tuple = chance.get_pro(Options.query_string)
            out_list = [time, score] + out_tuple[0]+out_tuple[1]
            for elem_index in range(len(out_list)):
                test_sheet6.write(sheet6_row, elem_index, out_list[elem_index])
            sheet6_row = sheet6_row + 1
        book.save('C:\\Users\\admin\\Desktop\\test5.xls')
        print(out_list)

        for score in range(98, 99):
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
            out_tuple = chance.get_pro(Options.query_string)
            out_list = [time, score] + out_tuple[0]+out_tuple[1]
            for elem_index in range(len(out_list)):
                test_sheet7.write(sheet7_row, elem_index, out_list[elem_index])
            sheet7_row = sheet7_row + 1
        book.save('C:\\Users\\admin\\Desktop\\test5.xls')
        print(out_list)


reliability_judge()
