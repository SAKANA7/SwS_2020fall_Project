# 2020/09/17 v0.0.0
# 2020/10/05 v0.0.1
# 2020/10/08 v0.0.2 等待验收
from tkinter import *
from tkinter import ttk,filedialog
from tkinter import scrolledtext,messagebox
import tkinter as tk
import math
import os
import multiprocessing
from tkinter.ttk import *
import r2_stringmatching
import r3_FunctionAnalysis
import r4_StackBuffer
import r5_FormatSring
import b1_heapbuffer
import b2_intengerwidth
import b3_IntengerCalOverfl
import b5_nullpointer
window = Tk()
window.title("SAKANA's project")
window.geometry('400x470')
'''frame1用来存储结果'''
frame1 = ttk.Frame(window, height = 90, width=380) # 信息区
frame1.grid(row=0,column=0, columnspan = 3 , padx=10, pady=5)
frame1.propagate(0)
result = scrolledtext.ScrolledText(frame1,width=51,height=10)
result.grid(column=0,row=0)

'''labelframe1用来存储同源性检测'''


labelframe1 = ttk.LabelFrame(window, text=' 同源性检测 ', height = 160, width=380) # 信息区
labelframe1.grid(row=1,column=0, columnspan = 3 , padx=10, pady=10,ipadx=5,ipady=5)
labelframe1.propagate(0) # 使组件大小不变，此时width才起作用

file1address=Entry(labelframe1, width=36)
file1address.grid(row=1,column=1,padx=5)
file2address=Entry(labelframe1, width=36)
file2address.grid(row=3,column=1,padx=5)

file1address.delete(0, END)  # 将输入框里面的内容清空
file1address.insert(0, '')
file1path=''
def getfile1():
    global file1path
    file1path= tk.filedialog.askopenfilename()
    print (file1path)
    file1address.delete(0, END)  # 将输入框里面的内容清空
    file1address.insert(0, file1path)
file2address.delete(0, END)  # 将输入框里面的内容清空
file2address.insert(0, '')
file2path=''
def getfile2():
    global file2path
    file2path= tk.filedialog.askopenfilename()
    print (file2path)
    file2address.delete(0, END)  # 将输入框里面的内容清空
    file2address.insert(0, file2path)
btn1 = ttk.Button(labelframe1, text="FILE1",command=getfile1)
btn1.grid(row=1,column=3)
btn2 = ttk.Button(labelframe1, text="FILE2",command=getfile2)
btn2.grid(row=3,column=3)
selected=IntVar()
radiobtn1 = Radiobutton(labelframe1, text='Homology',value=1,variable=selected)
radiobtn1.grid(row=5,column=1,sticky='w',padx=5)
radiobtn2 = Radiobutton(labelframe1, text='CFG',value=2,variable=selected)
radiobtn2.grid(row=6,column=1,sticky='w',padx=5)

def detect1():
    if file1path!='' and file2path!='':
        if selected.get()==1:
            simi=r2_stringmatching.stringmatching(file1path,file2path)
            result.delete(1.0,END)
            result.insert(1.0,'The similarity of these 2 files is:'+str(int(simi))+'%')
        elif selected.get()==2:
            simi=r3_FunctionAnalysis.FunctionAnalysis(file1path,file2path)
            if math.isnan(simi):
                result.delete(1.0,END)
                result.insert(1.0,'This file have no appropriate result,\nMaybe it is not an intact code.')
            else:
                result.delete(1.0,END)
                result.insert(1.0,'The similarity of these 2 files is:'+str(int(simi))+'%')
btn3 = Button(labelframe1, text="DETECT",command=detect1)
btn3.grid(row=5,column=3,rowspan=2)


labelframe1.grid_rowconfigure(2,minsize=5) # 调整两个控件之间的距离
labelframe1.grid_rowconfigure(4,minsize=5)
labelframe1.grid_columnconfigure(2,minsize=16)





'''labelframe2用来存储溢出检测'''
labelframe2 = ttk.LabelFrame(window, text=' 溢出检测 ', height = 200, width=380) # 信息区
labelframe2.grid(row=2,column=0, columnspan = 3 , padx=10, pady=10)
labelframe2.propagate(0) # 使组件大小不变，此时width才起作用
file3address=Entry(labelframe2, width=36)
file3address.grid(row=0,column=0,padx=5)

file3address.delete(0, END)  # 将输入框里面的内容清空
file3address.insert(0, '')
file3path=''
def getfile3():
    global file3path
    file3path= tk.filedialog.askopenfilename()
    print (file3path)
    file3address.delete(0, END)  # 将输入框里面的内容清空
    file3address.insert(0, file3path)

btn3 = ttk.Button(labelframe2, text="FILE3",command=getfile3)
btn3.grid(row=0,column=2,padx=5)
lb1 = ttk.Label(labelframe2, text = '  Function')
lb1.grid(row=1,column=0,sticky='w')
functionvar = StringVar()
functionlist = ttk.Combobox(labelframe2, textvariable=functionvar,width=33)
functionlist['values']=('StackBuffer','FormatString','HeapBuffer','IntegerWidth','IntegerCal','NullPointer')
functionlist.current(0)
functionlist.grid(row=2,column=0,padx=5,pady=5)

def detect2():
    print(file3path)
    if file3path!='':
        result.delete(1.0, END)
        if functionvar.get()=='StackBuffer':
            Suspicious_FunctionName_line=r4_StackBuffer.GetEvery_Begin_End(file3path)
            for name, line in Suspicious_FunctionName_line.items():
                result.insert(END, '警告:在以下文件行发现使用可疑函数 "'+name+'" :\n')
                result.insert(END,line)
                result.insert(END,'\n')
        elif functionvar.get()=='HeapBuffer':
            Suspicious_FunctionName_line=r4_StackBuffer.GetEvery_Begin_End(file3path)
            for name, line in Suspicious_FunctionName_line.items():
                result.insert(END, '警告:在以下文件行发现使用可疑函数 "'+name+'" :\n')
                result.insert(END,line)
                result.insert(END,'\n')
        elif functionvar.get()=='FormatString':
            suspicious_line1,suspicious_line2=r5_FormatSring.find_formatstring(file3path)
            if len(suspicious_line1)!=0:
                result.insert(END,'存在%n参数的可疑行数有:\n')
                result.insert(END,suspicious_line1)
                result.insert(END,'\n')
            if len(suspicious_line2)!=0:
                result.insert(END,'存在参数不匹配的可疑行数有:\n')
                result.insert(END,suspicious_line2)
                result.insert(END,'\n')
        elif functionvar.get()=='IntegerWidth':
            line=b2_intengerwidth.GetEvery_Begin_End(file3path)
            if len(line)==0:
                result.insert(END,'不存在可疑整数宽度溢出行.\n')
            else:
                result.insert(END,'存在整数宽度溢出可疑行数有:\n')
                result.insert(END,line)
        elif functionvar.get()=='IntegerCal':
            line=b3_IntengerCalOverfl.GetEvery_Begin_End(file3path)
            if len(line)==0:
                result.insert(END,'不存在可疑整数运算溢出行.\n')
            else:
                result.insert(END,'存在整数运算溢出可疑行数有:\n')
                result.insert(END,line)
        elif functionvar.get()=='NullPointer':
            line=b5_nullpointer.GetEvery_Begin_End(file3path)
            if len(line)==0:
                result.insert(END,'不存在空指针引用行.\n')
            else:
                result.insert(END,'存在空指针引用可疑行数有:\n')
                result.insert(END,line)


btn4 = ttk.Button(labelframe2, text="DETECT",command=detect2)
btn4.grid(row=2,column=2,padx=5)


# labelframe2.grid_rowconfigure(2,minsize=5) # 调整两个控件之间的距离
# labelframe2.grid_rowconfigure(0,minsize=5)
# labelframe2.grid_rowconfigure(4,minsize=5)
# labelframe2.grid_columnconfigure(0,minsize=5)
labelframe2.grid_columnconfigure(1,minsize=16)
# labelframe2.grid_columnconfigure(4,minsize=5)
'''最下面的三个按钮，分别为多进程和返回，还有打开导出文件'''
def quit1():
    quit1=messagebox.askokcancel('提示','真的要退出吗>_<?')
    if quit1==True:
        window.destroy()
def multi():
    pool = multiprocessing.Pool()
    multiresult = []
    temp=(file1path,file2path)
    multiresult.append(pool.apply_async(r3_FunctionAnalysis.FunctionAnalysis,temp).get())
    multiresult.append(pool.apply_async(r2_stringmatching.stringmatching,temp).get())
    result.delete(1.0, END)
    result.insert(END,multiresult)
    pool.close()
def openoutput():
    outputaddress='C:/Users/Lenovo/Desktop/SoftwareSecurity_2020fall_Project/output.txt'
    os.system(outputaddress)
btn7 = ttk.Button(window, text="OPEN OUTPUT",command=openoutput)
btn7.grid(row=3,column=2,pady=5,padx=20,sticky='w')
if __name__ == "__main__":
    btn5 = ttk.Button(window, text="QUIT",command=quit1)
    btn5.grid(row=3,column=0,pady=5,padx=20,sticky='w')
    btn6 = ttk.Button(window,text="MULTI",command=multi)
    btn6.grid(row=3,column=1,pady=5,sticky='w')
    window.mainloop()