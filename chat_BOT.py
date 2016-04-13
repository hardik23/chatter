from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import socket,threading,time

host="127.0.0.1"
port = 0
ttlock=threading.Lock()
shutdown=False
server=('127.0.0.1',5000)


connected=False

def receving(name,sock):
    while not shutdown:
        try:
            ttlock.acquire()
            while True:
                data,addr= s.recvfrom(1024)
                #print(str(data.decode())+"#")
                message_text.config(state=NORMAL)
                message_text.insert(END, str(data.decode()) + '\n')
                message_text.config(state=DISABLED)

        except:
            pass
        finally:
            ttlock.release()


def connect_me(event):
    if name_enter.get() !='':
        x.set('Connected=>Hi '+name_enter.get())
        global connected
        connected = True
        type_msg.focus()


        message_text['state'] = NORMAL
        message_text.delete(0.0, END)
        message_text['state'] = DISABLED
        s.sendto(str.encode("name"+name_enter.get()),server)
    else:
        pass

def clear_box():
    message_text['state']=NORMAL
    message_text.delete(0.0,END)
    message_text['state'] = DISABLED



def send_msg(event):
    if name_enter.get()!="" and connected:

        print(type_msg.get())
        s.sendto(str.encode(name_enter.get() + " : " + y.get()), server)
        type_msg.delete(0, END)

    else:
        message_text.config(state=NORMAL)
        message_text.insert(END, 'You are not connected buddy'+ '\n')
        message_text.config(state=DISABLED)
        type_msg.delete(0, END)

root=Tk()
y=StringVar()
bottom=Frame(root)
bottom.grid(column=0,row=0)

##################################################################################

top1=ttk.Frame(bottom)
top1.grid(row=0,rowspan=4,columnspan=5)

name=ttk.Label(top1,text='Name:')
name.grid(row=0,column=0,rowspan=1,columnspan=1)

name_enter=ttk.Entry(top1)
name_enter.grid(row=0,column=1,rowspan=1,columnspan=3,padx=5,pady=5)
name_enter.bind('<Return>',connect_me)
name_enter.focus()

connect=ttk.Button(top1,text="connect")
connect.grid(row=0,column=4,columnspan=1,padx=5,pady=5)
connect.bind('<Return>',connect_me)
connect.bind('<Button-1>',connect_me)

x=StringVar()
welcome=ttk.Label(top1,textvariable=x)
welcome.grid(row=2,column=3,columnspan=1)

cancel=ttk.Button(top1,text="clear")
cancel.grid(row=2,column=4,columnspan=1,padx=5,pady=5)

############################################################################

top2=ttk.Frame(bottom,height=5,width=5,borderwidth=3)
top2.grid(row=4,column=0,rowspan=3,columnspan=5)

message_text=ScrolledText(top2,height=15,width=40)
message_text.grid(row=0,column=0,columnspan=5)
message_text.config(state=DISABLED)

####################################################################

top3=ttk.Frame(bottom)
top3.grid(row=7,column=0,rowspan=1,columnspan=5)


type_msg=ttk.Entry(top3,textvariable=y,width=45)
type_msg.grid(row=0,column=0,columnspan=5)
type_msg.bind('<Return>',send_msg)

send=ttk.Button(top3,text="Send")
send.grid(row=1,column=0,padx=5,pady=5,sticky=W)
send.bind('<Button-1>',send_msg)

clear=ttk.Button(top3,text="Clear Box",command=clear_box)
clear.grid(row=1,column=2,padx=5,pady=5)


quit=ttk.Button(top3,text='quit',command=root.quit)
quit.grid(row=1,column=4,sticky=E,padx=5,pady=5)

###########################################################################################

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)
rt=threading.Thread(target=receving,args=("recvthread",s))
rt.start()


'''for w in top2.grid_slaves(column=6):
    print(w,'+')'''


root.mainloop()
s.close()
shutdown=True
rt.join()