# coding:utf8
import sys,random
import pygame
from socket import *

class worldenv:
    '''
    以图形模式，创建和绘制活动环境，并可以接纳cells的接入和装载
    '''
    def __init__(self, width, height):
        self.width, self.height = width, height     # 设置环境的总体大小：width和height
        self.size = 10                              # 统一cell的大小尺寸,default为10
        #self.envcells = []
        self.background = pygame.Surface((self.width * self.size, self.height * self.size))
        self.background.fill((20, 20, 20))

        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))

    def grow(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        '''
        n = 0
        for x in range(self.width):
            for y in range(self.height):
                if  len(self.envcells) < self.width * self.height:
                    self.envcells.append(envCell(self.size,n))
                    self.envcells[n].grid = {'x':x + 1,'y':y + 1}
                else:
                    self.envcells[n].grow()

            screen.blit(self.envcells[n].shape, ((x*self.size), (y*self.size)))
            n = n + 1
        '''

def server():
    HOST = '127.0.0.1'
    PORT = 10521
    ADDR = (HOST, PORT)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5)
    while True:
        print('Waiting for connecting ......')
        tcpclientsocket, addr = server_socket.accept()
        print('Connected by ', addr)

        while True:
            data = tcpclientsocket.recv(1024)
            if not data:
                break
            print(data)
            data = input('I>')
            data = data.encode(encoding="utf-8")
            tcpclientsocket.send(data)
        tcpclientsocket.close()
    server_socket.close()

pygame.init()
pygame.display.set_mode((600,600))
pygame.display.set_caption("Hello World!")
#clock = pygame.time.Clock()
#clock.tick(0.1)

env = worldenv(60,60)
pygame.display.flip()
