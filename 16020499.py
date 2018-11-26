import socket
from _thread import *

host = '127.0.0.1'
port = 5556
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((host, port))
except socket.error as e:
    print(str(e))


sock.listen(5)

print('waiting for connection')

def send_reply(conn,filename):
    reply = "HTTP/1.0 200 OK\r\n\n".encode()
    content = ''
    if filename == "/":
        file = open('index.html', 'rb')           
        content = file.read()
        reply += content

    else:
        filename = filename.strip("/")
        try:
            file=open(filename,'rb')
            content = file.read()
            reply += content
        except FileNotFoundError:
            reply='HTTP/1.0 404 Not found\r\n\n'.encode()
            file = open('404.html', 'rb')
            content = file.read()
            reply += content


    conn.sendall(reply)
    conn.close()


data = ''
while True:
    conn, addr = sock.accept()
    print('connected to:'+addr[0]+':'+str(addr[1]))
    while(True):
        data += conn.recv(2048).decode("utf-8")
        if(data.endswith("\r\n\r\n")):
            lines=data.splitlines()
            filename=lines[0].split(' ')[1]
            print("requested filename:" +filename)
            start_new_thread(send_reply, (conn,filename))
            data = ''
            break
        else:
            continue

    
