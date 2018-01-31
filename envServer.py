# coding:utf8
import sys,random
import pygame
from socket import *

class worldenv:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.size = 10
        self.envcells = []
        self.background = pygame.Surface((self.width * self.size, self.height * self.size))
        self.background.fill((20, 20, 20))

    def grow(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))

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

class envCell:
    '''
    Init cell: size,eng and shape
    '''

    def __init__(self, size, id):
        self.id = id
        self.size = size
        self.growStep = 1
        # -----------------------------------------------------
        # 可以设置环境元素的能量布局，布局不同，细胞会表现出不同行为特征
        # 1：均匀布局
        self.eng = 2000
        # 2：随机布局
        #self.eng = random.uniform(100, 2000)  # 最大值2550
        # 3：渐进布局
        # if self.id < 2550:
        #    self.eng = 2550 - self.id #random.uniform(100, 2000)
        # if self.id >= 2550:
        #    self.eng = 2000 #random.uniform(100, 2000)
        # -----------------------------------------------------

        self.grid = {}
        self.shape = pygame.Surface((self.size - 2, self.size - 2))
        self.color = (0, int(self.eng / self.size), 0)
        self.shape.fill(self.color)

        '''
        grow eng
        '''

    def grow(self):
        # 环境元素能量将变化，生长期+1能量,衰亡期-5能量；生长值上下极限能量范围100～2550，遇上而衰，遇下而生。
        if self.eng <= 100:
            self.growStep = 1
        if self.eng >= 2550:
            self.growStep = -5

        self.eng = self.eng + self.growStep
        # self.color = (0, int(self.eng/self.size), 0)    # 重置细胞留下的信息量为0
        b = self.color[2] - 3
        if b < 0: b = 0
        if b > 250: b = 250
        self.color = (self.color[0], int(self.eng / self.size), b)  # 这会一直保留细胞留下的信息量，并逐渐累计
        self.shape.fill(self.color)


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


server()