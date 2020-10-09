# 存在%n的，以及存在格式化符号与printf中输出参数不一致的。
# 2020/9/23 写完，但没有更复杂的样本来进行分析
def find_formatstring(address1):
    filein = open(address1, encoding='utf-8')# untitled7
    fileout = open(r"C:\Users\Lenovo\Desktop\SoftwareSecurity_2020fall_Project\output.txt", "w", encoding='utf-8')
    prefile = preprocess(filein)
    prefile = prefile.split('\n')
    # line1用来存储%n情况，line2用来存储参数不匹配情况
    suspicious_line1 = []
    suspicious_line2 = []
    index = 0
    # prefile只是一个用来和输出行数比对的文件，写入后就不需要对它进行任何研究操作了，在最后close即可
    for line in prefile:
        fileout.write(line)
        fileout.write('\n')
    for line in prefile:
        index += 1
        if "print" in line:
            if '%n' in line:
                suspicious_line1.append(index)
            temp1 = line.count("%")
            line.split("\"")
            # 以printf("%s,%d,%d,%s",buf,a,b); 为例,应该为line[2]但如果字符串中有对双引号转义就又不好说，所以只之后再想好办法吧
            temp2 = line[2].count(",")
            if temp1 != temp2:
                suspicious_line2.append(index)
    '''
    if len(suspicious_line1) != 0:
        print("存在%n参数的可疑行数有:")
        print (suspicious_line1)
    if len(suspicious_line2) != 0:
       print("存在参数不匹配的可疑行数有:")
       print(suspicious_line2)
    '''
    filein.close()
    fileout.close()
    return suspicious_line1,suspicious_line2


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


# find_formatstring()