# 2020/09/17 v0.0.0
import ply.lex as lex

# filein1是要检查的，filein2是基准的，这样能相对降低错误率，但实际上错误率还是很高的，因为比如return，for这种语句一般每个程序都会有。
def stringmatching(address1,address2):
    filein1 = open(address1, encoding='utf-8')
    prefile1 = preprocess(filein1)
    lexfile1 = mylex(prefile1)
    filein2 = open(address2, encoding='utf-8')
    prefile2 = preprocess(filein2)
    lexfile2 = mylex(prefile2)
    result = calculate(lexfile1, lexfile2)
    # print("similarity:%f%%" % result)
    return result


def preprocess(file):
    # before all functions, if typedef,put orign&new into a dic.
    dic = {}
    newTypelist = []
    line = file.readline()
    while line:
        if '#' in line or '/' in line:
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
        if '#' in line2 or '//' in line2 or 'typedef' in line2:
            """or /*"""
            pass
        else:
            place, res = typeexist(newTypelist, line2)
            if res:
                line2 = line2.replace(place, dic[place])
            tempfile += line2
        line2 = file.readline()
    return tempfile


def typeexist(list, line):
    for i in list:
        if i in line:
            return i, True
    return False, False


def mylex(data):
    reserved = {
        'if': '_IF',
        'char': '_CHAR',
        'short': '_SHORT',
        'int': '_INT',
        'long': '_LONG',
        'unsigned': '_UNSIGNED',
        'float': '_FLOAT',
        'double': '_DOUBLE',
        'while': '_WHILE',
        'for': '_FOR',
        'return': '_RETURN',
        'break': '_BREAK',
        'const': '_CONST',
        'continue': '_CONTINUE',
        'default': '_DEFAULT',
        'static': '_STATIC',
        'else': '_ELSE',
        'switch': '_SWITCH',
        'printf': '_PRINTF',
        'scanf': '_SCANF',
        'putchar': '_PUTCHAR',
        'getchar': '_GETCHAR',
        'gets': '_GETS',
        'puts': '_PUTS',
        'strlen': '_STRLEN',
        'strcpy': '_STRCPY',
        'strcmp': '_STRCMP',
        'malloc': '_MALLOC',
        'free': '_FREE',
    }
    tokens = [
                 'NUMBER',
                 'PLUS',
                 'MINUS',
                 'MULTI',
                 'DIVIDE',
                 'LARGER',
                 'LOWER',
                 'MOD',
                 'EQUAL',
                 'LSP',
                 'RSP',
                 'LP',
                 'RP',
                 'ID',
                 'CHARACTER',
                 'SEMI',
                 'COMA',
                 'COLON',
                 'EXCLA',
                 'BACKSLASH'
             ] + list(reserved.values())
    # 这个有不全，在t_error(t)时候有体现，以后再补充吧
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTI = r'\*'
    t_DIVIDE = r'/'
    t_LARGER = r'>'
    t_LOWER = r'<'
    t_EQUAL = r'='
    t_MOD = r'\%'
    t_LSP = r'\{'
    t_RSP = r'\}'
    t_LP = r'\('
    t_RP = r'\)'
    t_SEMI = r';'
    t_COMA = r','
    t_COLON = r'\"'
    t_EXCLA = r'!'
    t_BACKSLASH = r'\\'

    # A regular expression rule with some action code
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule 尝试不输出错误字符而是直接跳过
    def t_error(t):
        #print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')
        return t
    # 这个不是很懂其含义
    '''
    def t_CHARACTER(t):
        r"'.?'"
        return t
    '''

    # Build the lexer
    lexer = lex.lex()
    # input data
    lexer.input(data)
    # tokennize
    pre_line = 1
    result = ''
    # 从下面可以看出来，preprocess的时候其实并没去掉空格，是t_ignore和下面8行函数实现的，因为空格没被存在token里。
    while True:
        tok = lexer.token()
        if not tok:
            break
        if pre_line != tok.lineno:
            result += '\n'
            pre_line = tok.lineno
        result += tok.type
    return result


def calculate(lexfile1, lexfile2):
    similarities = 0
    count = 0
    file1list = []
    file2list = []
    file1list = lexfile1.splitlines()
    file2list = lexfile2.splitlines()
    totallines = len(file1list)
    file1listlen = len(file1list)
    file2listlen = len(file2list)
    for i in range(file1listlen):
        for j in range(file2listlen):
            if file1list[i] == file2list[j]:
                count += 1
                break
    similarities = count / file1listlen
    similarities = similarities * 100
    return similarities


# stringmatching('C:/Users/Lenovo/Desktop/SoftwareSecurity_2020fall_Project/Untitled3.c','C:/Users/Lenovo/Desktop/SoftwareSecurity_2020fall_Project/Untitled4.c')
