import pprint
from collections import defaultdict
import networkx as nx

# 问题在于如果并非完整的代码而是代码段，就不能够根据分析到函数体来确定是否为函数。
# 2020/9/19 已经实现识别出完整代码的图结构。有待完成：1.是否可以识别部分代码块的图结构 2.如何计算相似度
# 2020/9/30 第二次完善，希望使用networkx的计算图编辑距离来计算相似度，但还没有找到合适的公式
# 2020/10/2 第三次，联系到字符串编辑距离的公式:给定两个字符串a和b，已知求出来的编辑距离是distance,
# 则similarity=(1-distance/max(len(a),len(b))
# 因为是有向图，和字符串的区别是每个node间可以有两个edge，所以不妨把求出来的编辑距离/2，而len仍然是最大edge数
# 生成有向图 以字典形式
class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.items():  # python3: items(); python2: iteritems()
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))


def FunctionAnalysis(address1,address2):
    filein1 = open(address1, encoding='utf-8')
    prefile1 = preprocess(filein1)
    prefile1 = prefile1.split('\n')
    filein2 = open(address2, encoding='utf-8')
    prefile2 = preprocess(filein2)
    prefile2 = prefile2.split('\n')
    vertex1 = VertexJudge(prefile1)
    vertex2 = VertexJudge(prefile2)
    connections1 = init_connections(prefile1, vertex1)
    connections2 = init_connections(prefile2, vertex2)
    '''
    g1 = Graph(connections1, directed=True)
    g2 = Graph(connections2, directed=True)
    # similarities = calculate(g1, g2)
    # print(similarities)
    pretty_print = pprint.PrettyPrinter()
    pretty_print.pprint(g1._graph)
    pretty_print.pprint(g2._graph)
    '''
    gtest1 = nx.DiGraph()
    gtest2 = nx.DiGraph()
    gtest1.add_nodes_from(vertex1)
    gtest2.add_nodes_from(vertex2)
    gtest1.add_edges_from(connections1)
    gtest2.add_edges_from(connections2)
    gtest2_edges=gtest2.number_of_edges()
    gtest1_edges=gtest1.number_of_edges()
    tmp=(max(gtest1_edges,gtest2_edges))
    vmin=0.0

    for dist in nx.algorithms.similarity.optimize_graph_edit_distance(gtest1, gtest2):
        vmin=dist
    vmin/=2
    simi=(1-(vmin/tmp))*100
    # print("similarity: %f%%" % (simi))
    return simi


# 通过判断函数结构体的方式判断tempfile中的顶点:已定义的函数
def VertexJudge(tempfile):
    vertexs = []
    for line in tempfile:
        if '(' in line:
            if ('char' in line) or ('int' in line) or ('long' in line) or ('short' in line) or ('float' in line) or (
                    'double' in line) or ('void' in line) or ('signed' in line) or ('bool' in line):
                if ';' not in line:
                    name = get_function_name(line)
                    vertexs.append(name)
    return vertexs


# 获取函数名称：比如说bool judge_func(char str[max]), 则list1=['bool' 'judge_func(char','str[max])'
# 挺巧妙地避开了正则表达式。
# 找到含有'('则'judge_func(char',list2=['judge_func','char']
def get_function_name(line):
    temp_list1 = line.split(' ')
    for string in temp_list1:
        if '(' in string:
            temp_list2 = string.split('(')
            name = temp_list2[0]
            return name


# 这个返回的是一个列表，列表里面存储的是元组，元组的第一个元素代表函数名a，第二个元素代表在函数a里被调用的函数。
def init_connections(tempfile, vertexs):
    # stack用来统计大括号，当左右大括号数目相等，表示一个函数体结束。connections存储所有的连接边(有向)
    # i为一个索引，用来看这是第几个函数体，因为第一次VertexJudge的时候已经按顺序读入了函数结构体
    # tempfile.seek(0)
    stack = 0
    connections = []
    # print(vertexs)
    i = -1
    # 三个if先判断是否为函数体结构
    for line in tempfile:
        flag=1
        if '(' in line:
            if ('char' in line) or ('int' in line) or ('long' in line) or ('short' in line) or ('float' in line) or (
                    'double' in line) or ('void' in line) or ('signed' in line) or ('bool' in line):
                if ';' not in line:
                    # 如果满足这三个条件一定上一个函数体结束了，语法错误我们不考虑所以重新来定义name，以及stack归零
                    # 这里是有一个限制的：定义函数的时候{要在下面一行，否则无法根据不同的{的位置来判断stack是否要归零。
                    # 我的理解：因为不同的人编程风格不一样，所以对输入文件的风格要求应该是清晰的，在这里就要求{在下一行。
                    # 这属于细节问题，想尝试得到对于不同位置{都适用的方法，待所有功能完善之后再进行吧。
                    i += 1
                    name = vertexs[i]
                    stack = 0
                    '''
                        if stack == 0:
                        # 还不确定？name = get_function_name(line)
                        name = 0
                        '''

        # 先判断该行中是否存在vertexs里面的元素，如果存在就把(name,v)这个元组加入到connections里
        # stack != 0是确保进入了函数体内部
        if stack != 0:
            if any(v in line for v in vertexs):
                for v in vertexs:
                    if (v+'(') in line :
                        temp = (name, v)
                        connections.append(temp)
        if '{' in line:
            stack += 1
        if '}' in line:
            stack -= 1
        # 当函数结构体循环完,重置name，等待新的函数结构体出现
    return connections


# 恢复重定义,去除行前空格
def preprocess(file):
    # before all functions, if typedef,put orign&new into a dic.
    dic = {}
    newTypelist = []
    line = file.readline()
    while line:
        if '#' in line or '/' in line or '/*' in line:
            pass
        elif 'typedef' in line:
            originType = line.split(' ')[1]
            newType = line.split(' ')[2]
            newType = newType.strip(';')
            dic[newType] = originType
            newTypelist.append(newType)
        elif '{' in line:
            break
        line = file.readline()
    for key, value in dic.items():
        if dic.__contains__(value):
            dic[key] = dic[value]

    # Restore source code redefinition type to original type
    tempfile = ""
    file.seek(0)
    line2 = file.readline()
    while line2:
        if '#' in line2 or '//' in line2 or 'typedef' in line2 or '/*' in line2:
            """or /*"""
            pass
        else:
            place, res = typeexist(newTypelist, line2)
            if res:
                line2 = line2.replace(place, dic[place])
            tempfile += line2
        line2 = file.readline()
    return tempfile


# 在preprocess()里会用到的，用于恢复重定义
def typeexist(list, line):
    for i in list:
        if i in line:
            return i, True
    return False, False


def calculate(g1, g2):
    pass


# FunctionAnalysis('C:/Users/Lenovo/Desktop/SoftwareSecurity_2020fall_Project/Untitled3.c','C:/Users/Lenovo/Desktop/SoftwareSecurity_2020fall_Project/Untitled4.c')
