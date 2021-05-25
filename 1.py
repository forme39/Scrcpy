import os,subprocess
from tkinter import *
import tkinter.filedialog as fd


# def run_cmd(cmd):
#     p = os.popen(cmd, shell=True, stdin="PIPE", stdout="PIPE", stderr="STDOUT")
#     stdout, stderr = p.communicate()
#     return p.returncode, stdout.strip()
#     code, out = run_cmd('ls /')
#     if code:
#        print('命令执行成功')
#     else:print('命令执行失败')
#     sys.exit(1)

def adb():#执行adb命令
    adb = entry2.get()
    if adb :
        d = os.popen(adb)
        ans = d.read()
        #print(ans)
        text2.insert("end",ans)
        text2.insert("end",'\n')
    else:text2.insert("end","请输入命令")

def stopadb():#执行adb命令
    d=os.popen("ctrl+c")
    ans = d.read()
    text2.insert("end",ans)
    text2.insert("end","\n")

def device(): #查看设备名
    d = os.popen("adb devices")
    ans = d.read()
    match = re.findall('(.*)device$',ans,re.M|re.I)
    print(match)
    if match:
        text2.insert("end", match)
    else:
        text2.insert("end", "无设备连接")
    text2.insert("end",'\n')

def chosedevice():#选择设备执行shell
    devicename = name.get()
    adb="adb -s "+ devicename +" shell"
    d = os.popen(adb)
    ans = d.read()
    text2.insert("end",ans)
    text2.insert("end",'\n')

def ipadd(): #查看Ip
    devicename = name.get()
    d = os.popen("adb -s "+ devicename +" shell ifconfig")
    ans = d.read()
    match = re.search('192.[1-9]*.[1-9]*.[1-9]*',ans,re.M|re.I)
    print(match.group())
    text2.insert("end", match.group())
    text2.insert("end",'\n')

def connect():#无线匹配
    port = "8889"
    print(port)
    if name.get():
        d = os.popen("adb -s "+name.get()+" tcpip " + port)  # 打开端口
        if "error" in d.read():
            port+=1
            print(port)
            os.popen("adb -s " + name.get() + " tcpip " + port)
    else:#未指定设备 单设备不需要新port
        os.popen("adb tcpip " + port)  # 打开端口
    return port

def conWire():#无线连接
    if not ip.get():
        text2.insert("end", "无线连接请输入ip")
        text2.insert("end", "\n")
        return
    port = connect()
    # port="8889"
    # os.popen("adb tcpip "+port) #打开端口

    adb = "adb connect " + ip.get() +":"+port
    d = os.popen(adb) #无线连接设备
    ans = d.read().encode(encoding = "utf-8")
    print(ans)
    #text2.insert("end",d)
    print(checkVar.get())
    if speed.get() and checkVar.get()==1:
        os.popen("Scrcpy -s "+ ip.get() +":"+port +" -b "+ str(int(speed.get())*1000000) + " -S")
        text2.insert("end", "指定速度 息屏连接")
    elif checkVar.get()==1:
        os.popen("Scrcpy -s "+ ip.get() +":"+port + " -S")
        text2.insert("end", "息屏连接")

    else:os.popen("Scrcpy -s "+ ip.get() +":"+port)

def conUsb():#有线连接
    if speed.get() and name.get():
        print(speed.get()*1000000)
        adb = "Scrcpy -s "+ name.get() +" -b "+ str(int(speed.get())*1000000)
    elif name.get():adb = "Scrcpy -s "+ name.get()
    else:adb = "Scrcpy"
    d = os.popen(adb)
    ans = d.read()
    print(ans)
    text2.insert("end", ans)
    text2.insert("end",'\n')

if __name__=="__main__":
    # run_cmd("adb devices")
    root = Tk(className='Scrcpy -forme39')

    root.minsize(500, 600)
    #label1 = Label(root, text="请输入", font=('宋体', '10'))
    # button2 = Button(root, text="查看设备ip", command=lambda: ipadd())
    # button2.place(x=120,y=10,anchor='nw')

    button3 = Button(root, text="查看设备列表", command=lambda :device())
    button3.place(x=200,y=10,anchor='nw')

    nScreenWid, nScreenHei = root.maxsize()
    nCurWid = root.winfo_reqwidth()
    nCurHeight = root.winfo_reqheight()
    root.geometry(
        "{}x{}+{}+{}".format(nCurWid, nCurHeight, int(nScreenWid / 2 - nCurWid / 2), int(nScreenHei / 2 - nCurHeight / 2-200)))
    label3 = Label(root, text="请输入比特率(默认8m):", font=('宋体', '10'))
    label3.place(x=50,y=50,anchor='nw')

    speed = Entry(root,width='10') #比特率输入框
    speed.place(x=200,y=50,anchor='nw')

    label6 = Label(root, text="选定设备名:", font=('宋体', '10'))
    label6.place(x=50, y=80, anchor='nw')
    name = Entry(root,width='20') #设备名
    name.place(x=150,y=80,anchor='nw')
    findip = Button(root, text="查看设备ip", command=(lambda: ipadd()))
    findip.place(x=310, y=75, anchor='nw')

    checkVar = StringVar(value="0")
    screen = Checkbutton(root, text="息屏连接", variable=checkVar)
    screen.place(x=400, y=75, anchor='nw')

    label7 = Label(root, text="输入目标ip地址:", font=('宋体', '10'))
    label7.place(x=30, y=110, anchor='nw')
    ip = Entry(root, width='20')  # ip
    ip.place(x=150, y=110, anchor='nw')

    con = Button(root, text="无线连接", command=(lambda: conWire()))
    con.place(x=310, y=110, anchor='nw')

    con2 = Button(root, text="usb连接", command=(lambda: conUsb()))
    con2.place(x=380, y=110, anchor='nw')

    label4 = Label(root, text="请输入adb命令:", font=('宋体', '10'))
    label4.place(x=200,y=140,anchor='nw')
    entry2 = Entry(root,width='65') #adb文本框
    entry2.place(x=20,y=165,anchor='nw')

    runadb = Button(root, text="执行adb命令", command=(lambda: adb()))
    runadb.place(x=155, y=190, anchor='nw')
    stop = Button(root, text="终止", command=(lambda: stopadb()))
    stop.place(x=300, y=190, anchor='nw')

    label5 = Label(root, text="执行命令结果", font=('宋体', '10'))
    label5.place(x=200,y=230,anchor='nw')

    text2 = Text(root, width='65', height='25') #返回信息文本框
    #滑动条
    scrollbar=Scrollbar(root)
    scrollbar.place(relwidth = 0.03, relheight = 0.59, relx = 0.96, rely = 0.41)
    scrollbar.config(command=text2.yview)
    text2.config(yscrollcommand=scrollbar.set,wrap=WORD)
    text2.place(x=20,y=250,anchor='nw')


    root.mainloop()