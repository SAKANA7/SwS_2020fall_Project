# 完成时间：2020/9/27，需要注意的样例就是，只接受int temp ;这样类似的定义。
# 这个的受限还是在于：如果是定义和赋值在一起，那就难以判别，
# 比如说unsigned short total = strlen(argv[1]) + strlen(argv[2]) + 1; 可以，但是如果 +换成* 会被我的指针判别机制导致无法识别。
# 遍历一遍代码，获取所有函数名,用vertexs[]存储
def VertexJudge(tempfile):
    vertexs = []
    index = 0 # 获取行数的索引，从1开始
    for line in tempfile:
        index += 1
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


def GetEvery_Begin_End(address1):
    filein = open(address1, encoding='utf-8')# b3in
    fileout = open(r"C:\Users\Lenovo\Desktop\SoftwareSecurity_2020fall_Project\output.txt","w", encoding='utf-8')
    prefile = preprocess(filein)
    prefile = prefile.split('\n')
    for line in prefile:
        fileout.write(line)
        fileout.write('\n')
    Vertexs = VertexJudge(prefile)
    # print(Vertexs)
    # FunctionName_BeginEnd, Suspicious_FunctionName_line =init_dics(prefile, Vertexs)
    # print(FunctionName_BeginEnd)
    # print(Suspicious_FunctionName_line)
    warningposition=GetEveryCalLine(prefile)
    # print("Warning: These lines have the risk of intenger calculate overflow!")
    # print(warningposition)
    return warningposition
    filein.close()
    fileout.close()


# 找到类似于样例里的敏感行
def GetEveryCalLine(tempfile):
    linenum=0
    CalLine=[]
    for line in tempfile:
        linenum += 1
        # 避免出现 char* buffer = (char*)malloc(total); 这种仍然被记入的情况, 但是myarray = malloc(len*sizeof(int));还会被计入
        if ('char' in line) or ('int' in line) or ('long' in line) or ('short' in line) or ('float' in line) or (
                'double' in line) or ('void' in line) or ('signed' in line) or ('bool' in line):
            if '*' in line and 'sizeof' not in line:
                continue
        if '*' in line or '+' in line:
            if '++' in line:
                continue
            # 常规的加法乘法运算 如a = b * c
            if '=' in line:
                CalLine.append(linenum)
    return CalLine
# 对赋值进行检测，如果宽整形到窄整形转换出现，就提示存在宽度溢出可能。
# 另一种想法，看敏感函数，然后再看敏感函数里的参数，然后在字典里寻找和找到宽窄整形转换。(感觉这个不应该考虑，复杂化了)


def init_dics(tempfile, Vertexs):
    # stack用来统计大括号，当左右大括号数目相等，表示一个函数体结束。connections存储所有的连接边(有向)
    # i为一个索引，用来看这是第几个函数体，因为第一次VertexJudge的时候已经按顺序读入了函数结构体
    # tempfile.seek(0)
    # 定义所有可疑函数的列表
    suspicious_functions=['strcpy(', 'strncpy(', 'mecpy(', 'memncpy(','strcat(', 'strncat(','sprintf(','vsprintf(',
                          'gets(','getchar(','read(','sscanf(','fscanf(','vfscanf(','vscanf(','vsscanf(']
    stack = 0
    # Begin 和End按顺序记录函数体的开始行和结束行，FunctionName_BeginEnd是一个字典用来存储{'函数名':[开始行,结束行]}，即{vertexs[i]:[Begin[i],End[i]]} for i in range(len(Begin))
    #BeginEnd直接存储[开始位置,结束位置]
    Begin = []
    End = []
    FunctionName_BeginEnd = {}
    BeginEnd=[]
    Suspicious_FunctionName_line = {} # FunctionName指可疑函数名，{'FunctionName':line}，这个line应该以数组形式存在，然后每次找到FunctionName时候初始化一个，再append()
    # print(vertexs)
    i = -1
    index = 0
    # 三个if先判断是否为函数体结构
    for line in tempfile:
        flag = 2 #无关紧要的数字，代表着不是刚刚开始也不是刚刚结束
        index += 1
        if '(' in line:
            if ('char' in line) or ('int' in line) or ('long' in line) or ('short' in line) or ('float' in line) or (
                    'double' in line) or ('void' in line) or ('signed' in line) or ('bool' in line):
                if ';' not in line:
                    # 如果满足这三个条件一定上一个函数体结束了，语法错误我们不考虑所以重新来定义name，以及stack归零
                    i += 1
                    Begin.append(index)
                    stack = 0
                    #flag ==1 代表着函数体刚刚开始
                    flag == 1
        # 先判断该行中是否存在vertexs里面的元素，如果存在就把(name,v)这个元组加入到connections里
        # stack != 0是确保进入了函数体内部
        if stack != 0:
            # 该行是否存在可疑函数
            if any(function in line for function in suspicious_functions):
                # 遍历每一个可疑函数名字
                for function in suspicious_functions:
                    # 如果可疑函数在行里
                    if function in line:
                        # 如果可疑函数的名字已经存在FunctionName_line里，只需要在value的列表里添加行数i
                        if function in Suspicious_FunctionName_line.keys():
                            Suspicious_FunctionName_line[function.rstrip('(')].append(index)
                        # 如果没有，需要定义一个列表存储i，然后定义键值对'可疑函数名':行数i
                        else:
                            temp = [index]
                            Suspicious_FunctionName_line[function.rstrip('(')] = temp
        if '{' in line:
            stack += 1
        if '}' in line:
            stack -= 1
            if stack == 0:
                flag = 0 # flag == 0代表函数体刚刚结束
        if stack == 0 and flag == 0:
            End.append(index)
            BeginEnd.append(Begin[i])
            BeginEnd.append(End[i])
            FunctionName_BeginEnd[Vertexs[i]]=BeginEnd
        BeginEnd=[]

        # 当函数结构体循环完,重置name，等待新的函数结构体出现
    return FunctionName_BeginEnd, Suspicious_FunctionName_line

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

# GetEvery_Begin_End()