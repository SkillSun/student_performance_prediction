# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 11:53:03 2017

@author: Skill Sun

公用设置文件,用于存放公用设置
"""


class Options:
    # 当前表格是否只有总评？
    IS_ONLY_SUMMARY = False
    # 分层脚本的输入文件路径
    PRE_IN_FILE_ROUTE = 'C:\\Users\\admin\\Desktop\\开发数据\\学生行为模式分析\\1.得到并整理学生数据\\3.最终整理好的学生作业+成绩数据\\平时+期末+总评.xls'
    # 分层脚本的输出文件夹路径
    PRE_OUT_FILE_DIRECTORY = "C:\\Users\\admin\\Desktop\\output\\"
    # 时间评级关系(评价得分高于key则为value)
    TIME_PERCENTAGE_LIST = [
        [50, '早'],
        [0, '晚']
    ]
    # 成绩评级关系(评价得分高于key则为value)
    SCORE_PERCENTAGE_LIST = [
        [50, '及格'],
        [0, '不及格']
    ]

    # 先验属性所在列下标
    pre_index_list = [i for i in range(5, 21)]
    # 后验属性所在列下标
    aft_index_list = [2, 3, 4]
    # 判定字符串
    query_string = '及格 晚 及格 晚 及格 晚 不及格 晚 及格 晚 及格 晚 及格 晚 不及格 晚'
