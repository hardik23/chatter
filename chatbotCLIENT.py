#client chatbot

import socket,threading,time

host="127.0.0.1"
port = 0

ttlock=threading.Lock()
shutdown=False

def receving(name,sock):
    while not shutdown:
        try:
            ttlock.acquire()
            while True:
                data,addr= s.recvfrom(1024)
                print(str(data.decode())+"#")
        except:
            pass
        finally:
            ttlock.release()


server=('127.0.0.1',5000)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

rt=threading.Thread(target=receving,args=("recvthread",s))
rt.start()

alias=input("Name : ")
while 1:
    if alias!='':
        s.sendto(str.encode("name:"+alias),server)
        break
    else:
        alias=input("Name :")
message = input("tell ")

while message !='q':
    if message!='':
        s.sendto(str.encode(alias+" : "+message),server)
    #ttlock.acquire()
    message = input()
    #ttlock.release()
    time.sleep(0.2)

shutdown=True
rt.join()
s.close()


