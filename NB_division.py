# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:29:34 2017

@author: Skill Sun
"""
from NB_options import Options


# 属性结点
class AttrNode:
    def __init__(self, attr_name):
        # 该属性的名称
        self.attr_name = attr_name
        # 该属性的情况列表
        self.con_list = []


# 属性情况结点
class ConNode:
    def __init__(self, attr_name, con_name, times=1):
        # 该情况所从属的属性名
        self.attr_name = attr_name
        # 该结点的情况名
        self.con_name = con_name
        # 该情况的出现次数
        self.times = times


# 条件概率表结点
class ChanceGraph:
    def __init__(self, pre_attr_node, aft_attr_node):
        self.pre_attr_node = pre_attr_node
        self.aft_attr_node = aft_attr_node
        self.graph = []

    def get_chance(self, pre_str):
        pre_index = 0
        for pre_con_node in self.pre_attr_node.con_list:
            if pre_con_node.con_name == pre_str:
                break
            else:
                pre_index = pre_index + 1
        else:
            raise Exception
        return self.graph[pre_index]


# 朴素贝叶斯分类类
class NBDivision:
    def __init__(self, file_str=Options.PRE_OUT_FILE_DIRECTORY,
                 pre_list=Options.pre_index_list,
                 aft_list=Options.aft_index_list,
                 test_reliability=False
                 ):
        # 文件目录
        self.file_str = file_str
        # 先验属性列表
        self.pre_list = pre_list
        # 后验属性列表
        self.aft_list = aft_list
        # 所有属性列表
        self.total_attr = []
        # 所有样本数据
        self.total_data = []
        # 属性名到属性状态列表和出现次数的映射
        self.total_attr_nodes = []
        # 所有条件概率，四维列表
        self.total_chance = []
        # 是否进行分层可靠性测试
        self.test_reliability = test_reliability

        if self.test_reliability:
            # 执行读取文件操作, 初始化self.total_data和self.total_attr
            self.read_file()
            pass
        else:
            # 执行读取文件操作, 初始化self.total_data和self.total_attr
            self.read_file()
            # 执行整理属性操作, 初始化self.attr_nodes和其中的con_nodes
            self.calc_attr()
            # 执行初始化概率表操作, 初始化self.total_chance
            self.calc_chance()

    # 初始化self.total_data和self.total_attr
    def read_file(self):
        file = open(self.file_str+'\\0.txt')
        line = file.readline()
        if line:
            # 第一行数据给total_attr
            self.total_attr = line.split()
        else:
            file.close()
            raise EOFError
        line = file.readline()
        while line:
            # 其他行数据给total_data
            data = line.split()
            self.total_data.append(data)
            line = file.readline()
        file.close()
        # Debugged.

    # 初始化self.attr_nodes
    def calc_attr(self):
        # 把属性结点赋值给属性情况列表
        for attr in self.total_attr:
            attr_node = AttrNode(attr)
            self.total_attr_nodes.append(attr_node)
        # 遍历数据,得到每个属性的所有情况和该情况的出现次数
        for data_line in self.total_data:
            for attr_index in self.pre_list + self.aft_list:
                new_con_name = data_line[attr_index]
                for exist_con_node in self.total_attr_nodes[attr_index].con_list:
                    if exist_con_node.con_name == new_con_name:
                        exist_con_node.times = exist_con_node.times + 1
                        break
                    else:
                        continue
                else:
                    new_con_node = ConNode(self.total_attr_nodes[attr_index].attr_name, new_con_name)
                    self.total_attr_nodes[attr_index].con_list.append(new_con_node)
                # Debugged.

    # 初始化self.total_chance
    def calc_chance(self):
        for pre_index in self.pre_list:
            for aft_index in self.aft_list:
                pre_attr_node = self.total_attr_nodes[pre_index]
                aft_attr_node = self.total_attr_nodes[aft_index]
                graph = ChanceGraph(pre_attr_node, aft_attr_node)
                for pre_con_node in pre_attr_node.con_list:
                    chance_list = []
                    for aft_con_node in aft_attr_node.con_list:
                        base = aft_con_node.times
                        show = 0.000001
                        for data_line in self.total_data:
                            if data_line[pre_index] == pre_con_node.con_name:
                                if data_line[aft_index] == aft_con_node.con_name:
                                    show = show + 1
                        chance_list.append(show / base)
                    graph.graph.append(chance_list)
                self.total_chance.append(graph)
                # Debugged.

    # 计算发生的条件概率集合
    # 返回值为[[第一个后验属性的第一种情况的出现概率,第一个后验属性的第二种情况的出现概率...][第二个后验属性...]]
    def get_condition_pro(self, query_str):
        query_list = query_str.split()
        final = []
        for aft_index in range(len(self.aft_list)):
            cur_aft_result = []
            for pre_index in range(len(self.pre_list)):
                graph_node = self.total_chance[len(self.aft_list) * pre_index + aft_index]
                chance_list = graph_node.get_chance(query_list[pre_index])
                if cur_aft_result:
                    for index in range(len(chance_list)):
                        cur_aft_result[index] = cur_aft_result[index] * chance_list[index]
                else:
                    cur_aft_result = chance_list
            final.append(cur_aft_result)
        return final

    # 计算后验属性的每种状况的概率
    def get_aft_con_pro(self):
        final = []
        for aft_index in self.aft_list:
            attr_node = self.total_attr_nodes[aft_index]
            result = []
            for con_node in attr_node.con_list:
                result.append(con_node.times / len(self.total_data))
            final.append(result)
        return final

    # 计算最终给的条件概率
    def get_pro(self, query_str):
        # 条件概率列表
        con_list = self.get_condition_pro(query_str)
        # 后验属性出现概率列表
        aft_list = self.get_aft_con_pro()
        result = []
        name = []
        for list_index in range(len(con_list)):
            for elem_index in range(len(con_list[list_index])):
                result.append(con_list[list_index][elem_index] * aft_list[list_index][elem_index])
        for attr_index in self.aft_list:
            attr_node = self.total_attr_nodes[attr_index]
            name.append(self.total_attr_nodes[attr_index].attr_name)
            for con_node in attr_node.con_list:
                name.append(con_node.con_name)
        return name, result


# 测试用脚本
"""
pre_index_list = Options.pre_index_list
aft_index_list = Options.aft_index_list
test = NBDivision('C:\\Users\\admin\\Desktop\\0.txt', pre_index_list, aft_index_list)
query_string = Options.query_string
print(test.get_pro(query_string))

print('Debug.')
"""
