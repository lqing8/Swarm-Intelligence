# coding:utf8
'''''创建客户端程序，向服务器传递数据'''

from socket import *


def client():
    HOST = '127.0.0.1'
    PORT = 10521

    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((HOST, PORT))
    while True:
        data = input('>')
        if not data:
            break
        clientsocket.send(data.encode(encoding="utf-8"))
        data = clientsocket.recv(1024)
        if not data:
            break
        print(data)



client()