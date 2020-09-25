import pprint
from collections import defaultdict
import networkx as nx

# 问题在于如果并非完整的代码而是代码段，就不能够根据分析到函数体来确定是否为函数。
# 2020/9/19 已经实现识别出完整代码的图结构。有待完成：1.是否可以识别部分代码块的图结构 2.如何计算相似度
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


def FunctionAnalysis():
    filein1 = open(r"C:\Users\Lenovo\Desktop\SoftwareSecurity_2020fall_Project\Untitled4.c", encoding='utf-8')
    prefile1 = preprocess(filein1)
    prefile1 = prefile1.split('\n')
    filein2 = open(r"C:\Users\Lenovo\Desktop\SoftwareSecurity_2020fall_Project\Untitled3.c", encoding='utf-8')
    prefile2 = preprocess(filein2)
    prefile2 = prefile2.split('\n')
    vertex1 = VertexJudge(prefile1)
    vertex2 = VertexJudge(prefile2)
    connections1 = init_connections(prefile1, vertex1)
    connections2 = init_connections(prefile2, vertex2)
    g1 = Graph(connections1, directed=True)
    g2 = Graph(connections2, directed=True)
    # similarities = calculate(g1, g2)
    # print(similarities)
    pretty_print = pprint.PrettyPrinter()
    pretty_print.pprint(g1._graph)
    pretty_print.pprint(g2._graph)


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
# 找到含有'('则'judge_func(char',list2=['judge_func','char']
def get_function_name(line):
    temp_list1 = line.split(' ')
    for string in temp_list1:
        if '(' in string:
            temp_list2 = string.split('(')
            name = temp_list2[0]
            return name


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

        if '(' in line:
            if ('char' in line) or ('int' in line) or ('long' in line) or ('short' in line) or ('float' in line) or (
                    'double' in line) or ('void' in line) or ('signed' in line) or ('bool' in line):
                if ';' not in line:
                    # 如果满足这三个条件一定上一个函数体结束了，语法错误我们不考虑所以重新来定义name，以及stack归零
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


FunctionAnalysis()
