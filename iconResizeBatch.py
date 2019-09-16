from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import scrolledtext
import os

root = tk.Tk()
pread = tk.StringVar()
pread2 = tk.StringVar()
pathexport = tk.StringVar()
pathread = tk.StringVar()
imagename = tk.StringVar()
comvalue = tk.StringVar()
comvalue2 = tk.StringVar()
output_type = 'png'
platindex = 0
platNameList = ["_Android_", "_Desktop_", "_iOS_", "_iPad_"]
sizeList = [[32, 48, 72, 96, 144, 192],
            [16, 32, 48, 128, 256],
            [29, 58, 57, 60, 75, 80, 87, 114, 120, 152, 180,  512, 1024],
            [40, 48, 72, 76, 50, 100, 144, 167]]


def scrprint(scrtarget, scrtext, insertloc='end'):
    scrtarget.configure(state='normal')
    scrtarget.insert(insertloc, scrtext)
    scrtarget.configure(state='disable')


def extractPath(input_path):
    indexloc = len(input_path)
    global pathexport
    global imagename
    for i in range(len(input_path)-1, -1, -1):
        if input_path[i] == '/':
            indexloc = i
            break
    pathexport = input_path[0:indexloc+1]
    for i in range(len(input_path)-1, -1, -1):
        if input_path[i] == '.':
            indexloc2 = i
            break
    imagename = input_path[indexloc+1:indexloc2]
    pathexport = pathexport + imagename + "_iconPack/"


def selectFile():
    try:
        global pathread
        pathread = askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        extractPath(pathread)
        if not pathread:
            scrprint(scr, '打开图片失败！\n')
            return
        else:
            global pathexport
            pread.set(pathread)
            pread2.set(pathexport)
            scrprint(scr, '已成功选择图片： ')
            scrprint(scr, pathread + '\n')
            scrprint(scr, '已成功选择输出路径： ')
            scrprint(scr, pathexport + '\n')
    except:
        scrprint(scr, '打开图片失败！\n')
        return


def selectPath():
    try:
        global pathexport
        pathexport = askdirectory()
        pathexport = pathexport + '/'
        if not pathexport:
            scrprint(scr, '打开路径失败！\n')
            return
        else:
            pread2.set(pathexport)
            scrprint(scr, '已成功选择输出路径： ')
            scrprint(scr, pathexport + '\n')
    except:
        scrprint(scr, '打开路径失败！\n')
        return


def typeSelect(*args):
    scrprint(scr, ['切换输出格式为', comboxlist.get()])
    scrprint(scr, '\n')


def printSizeSet():
    global sizeList
    global platindex
    for each in range(0, len(sizeList[platindex])):
        scrprint(scr, str(each+1))
        scrprint(scr, ". ")
        scrprint(scr, str(sizeList[platindex][each]))
        scrprint(scr, "x")
        scrprint(scr, str(sizeList[platindex][each]))
        scrprint(scr, '\n')


def typeSelect2(*args):
    scrprint(scr, '\n**************切换输出平台为')
    scrprint(scr, comboxlist2.get())
    scrprint(scr, '**************\n\n')
    global platindex
    if "Android" in comboxlist2.get():
        platindex = 0
    elif "Desktop" in comboxlist2.get():
        platindex = 1
    elif "iOS" in comboxlist2.get():
        platindex = 2
    elif "iPad" in comboxlist2.get():
        platindex = 3

    printSizeSet()
    scrprint(scr, '\n')



def resizeAndOutputImage(rsz_width, rsz_height, img_input):
    # print('Resize Source Image', img_input.size, 'to', rsz_width, 'x', rsz_height)
    img_output = img_input.resize((rsz_width, rsz_height), Image.ANTIALIAS)
    global imagename
    global platindex
    newname = imagename + platNameList[platindex] + str(rsz_width) + 'x' + str(rsz_height)
    global output_type
    global pathexport
    if not os.path.exists(pathexport):
        os.makedirs(pathexport)
    try:
        img_output.save(pathexport + newname+'.'+output_type)
        scrprint(scr, ['输出图片：', pathexport + newname+'.'+output_type])
        scrprint(scr, '\n')
    except:
        scrprint(scr, '输出错误！\n')


def processImage():
    global pathread
    global pathexport
    pathread = pread.get()
    pathexport = pread2.get()
    if (not pathread) or (not pathexport):
        scrprint(scr, '路径错误，请重新输入！\n')
        return
    global comvalue
    comv = comvalue.get()
    if not(comv == 'png' or comv == 'jpg' or comv == 'gif' or comv == 'bmp' or comv == 'ico'):
        scrprint(scr, '输出图像格式非法，请重新输入！\n')
        return
    global output_type
    output_type = comv
    try:
        img_input = Image.open(pathread)
    except:
        scrprint(scr, '图片读取失败！\n')
        return
    scrprint(scr, '\n******************开始处理图片******************\n\n')

    global sizeList
    global platindex
    for each in range(0, len(sizeList[platindex])):
        resizeAndOutputImage(sizeList[platindex][each], sizeList[platindex][each], img_input)

    scrprint(scr, '\n*******************任务已完成*******************\n\n')


root.title("FanKetchup批量图标生成器")
canvas = tk.Canvas(root, width=600, height=500)
canvas.pack()
frame1 = tk.Frame(master=root)
frame1.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')

entry1 = tk.Entry(master=frame1, textvariable=pread)
entry1.place(relwidth=0.7, relheight=0.05, relx=0.05, rely=0.1, anchor='nw')
button1 = tk.Button(master=frame1, text="选择待处理图片", command=selectFile)
button1.place(relwidth=0.15, relheight=0.05, relx=0.8, rely=0.1, anchor='nw')

entry2 = tk.Entry(master=frame1, textvariable=pread2)
entry2.place(relwidth=0.7, relheight=0.05, relx=0.05, rely=0.2, anchor='nw')
button2 = tk.Button(master=frame1, text="选择输出路径", command=selectPath)
button2.place(relwidth=0.15, relheight=0.05, relx=0.8, rely=0.2, anchor='nw')

scr = scrolledtext.ScrolledText(master=frame1, width=20, height=10)
scr.place(relwidth=0.9, relheight=0.55, relx=0.05, rely=0.3, anchor='nw')

button3 = tk.Button(master=frame1, text="开始处理", command=processImage)
button3.place(relwidth=0.15, relheight=0.08, relx=0.8, rely=0.9, anchor='nw')


comboxlist = ttk.Combobox(master=frame1, textvariable=comvalue)  # 初始化
comboxlist["values"] = ("png", "jpg", "gif", "bmp", "ico")
comboxlist.current(0)  # 选择第一个
comboxlist.bind("<<ComboboxSelected>>", typeSelect)  # 绑定事件
comboxlist.place(relwidth=0.15, relheight=0.05, relx=0.2, rely=0.88, anchor='nw')

comboxlist2 = ttk.Combobox(master=frame1, textvariable=comvalue2)  # 初始化
comboxlist2["values"] = ("Android图标", "Desktop图标", "iOS图标", "iPad图标")
comboxlist2.current(0)  # 选择第一个
comboxlist2.bind("<<ComboboxSelected>>", typeSelect2)  # 绑定事件
comboxlist2.place(relwidth=0.25, relheight=0.05, relx=0.4, rely=0.88, anchor='nw')

label1text = tk.StringVar()
label1text.set("图片输出设置：")
label1 = tk.Label(master=frame1, textvariable=label1text)
label1.place(relwidth=0.15, relheight=0.05, relx=0.05, rely=0.88, anchor='nw')

label2text = tk.StringVar()
label2text.set("多尺寸图标批量生成器 by FanKetchup")
label2 = tk.Label(master=frame1, textvariable=label2text)
label2.place(relwidth=0.4, relheight=0.05, relx=0.03, rely=0.02, anchor='nw')

scrprint(scr, '********欢迎使用FanKetchup自制的图标批量制作器************\n\n')
scrprint(scr, '该程序现在会将源图片批量输出为Android应用图标所需大小：\n\n')
printSizeSet()
scrprint(scr, '\n************请先选择源图片和输出路径**************\n\n')

frame1.tkraise()
root.mainloop()

# PackIns: pyinstaller -F -w --icon=FanAPP.ico iconResizeBatch.py
