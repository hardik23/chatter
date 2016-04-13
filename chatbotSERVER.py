#chatbot server

host="127.0.0.1"
port = 5000
import socket
import time

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)
print('server started')
client=[]
quitting=False
while not quitting:
    try:
        data,addr=s.recvfrom(1024)
        print('connected ')
        '''if "quit" in data:
            quitting=True'''
        if addr not in client:
            client.append(addr)

        print(time.ctime(time.time()) + str(addr)+" : " + str(data.decode()))
        for clients in client:
            if "name" not in data.decode():
                s.sendto(data,clients)

    except:pass

s.close()
