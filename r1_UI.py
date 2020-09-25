# 2020/09/17 v0.0.0
from tkinter import *
from tkinter.ttk import *
import r2_stringmatching
window = Tk()
window.title("SAKANA's project")
window.geometry('800x450')


lblhomology = Label(window,text="同源性分析:")
lblhomology.grid(column=0, row=0)
txtfile1adress=Entry(window, width=30)
txtfile1adress.grid(column=0, row=1)
txtfile2adress=Entry(window, width=30)
txtfile2adress.grid(column=0, row=2)
lbloutput = Label(window, text="Hello!Choose any function u need!")
# lbloutput = Label(window, text="Hello!Choose any function u need!", font=("Arial Bold", 12))
lbloutput.grid(column=0, row=3)

def R2clicked():
    similarity = r2_stringmatching.stringmatching()
    lbloutput.configure(text ="The similarity of 2 files is:" + str(similarity) + "%")
def R3clicked():
    pass
def File1addressclicked():
    pass
def File2addressclicked():
    pass
def ErrorSourceAddressclicked():
    pass

File1addressbtn =Button(window, text="TargetFile", command=File1addressclicked)
File1addressbtn.grid(column=30, row=1)
File2addressbtn =Button(window, text="SourceFile", command=File2addressclicked)
File2addressbtn.grid(column=30, row=2)
R2btn = Button(window, text="String Analysis",  command=R2clicked)
R2btn.grid(column=0, row=4)
R3btn = Button(window, text="CFG Analysis",  command=R3clicked)
R3btn.grid(column=10, row=4)
lblloophole = Label(window,text="漏洞分析:")
lblloophole.grid(column=0, row=5)
ErrorSourceAddressbtn =Button(window, text="ErrorSource", command=ErrorSourceAddressclicked)
ErrorSourceAddressbtn.grid(column=30, row=6)
ErrorSourceAddress=Entry(window, width=30)
ErrorSourceAddress.grid(column=0, row=6)

window.mainloop()