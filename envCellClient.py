# coding:utf8
import sys,random
import pygame
from socket import *

class envCell:
    '''
    Init cell: size,eng and shape
    '''

    def __init__(self, id, size, clock, coordinate):
        self.id = id                    #envCell 的唯一标识符ID
        self.size = 10                  #正方形图形大小尺寸，default 10
        self.clock = clock              #时钟频率（秒）
        self.energyStep = 1             #能量单元
        self.coordinate = coordinate    #在环境中的位置坐标

        if(size != None): self.size = size
        # -----------------------------------------------------
        # 可以设置环境元素的能量布局，布局不同，细胞会表现出不同行为特征
        # 1：常量
        self.energy = 2000
        # 2：随机
        #self.energy = random.uniform(100, 2000)  # 最大值2550
        # 3：条件
        # if self.id < 2550:
        #    self.energy = 2550 - self.id #random.uniform(100, 2000)
        # if self.id >= 2550:
        #    self.energy = 2000 #random.uniform(100, 2000)
        # -----------------------------------------------------

        self.color = (0, int(self.energy / self.size), 0)  #将能量通过green color显示出来
        # 绘制envCell
        self.shape = pygame.Surface((self.size - 2, self.size - 2))
        self.shape.fill(self.color)

    '''
        嵌入到环境中，和服务器通讯（infomation receive and send）
    '''
    def createclient(self, HOST, PORT):
        # connected server
        clientsocket = socket(AF_INET, SOCK_STREAM)
        clientsocket.connect((HOST, PORT))

        # listen in ...
        while True:
            data = input('>')
            if not data:
                break
            clientsocket.send(data.encode(encoding="utf-8"))
            data = clientsocket.recv(1024)
            if not data:
                break
            print(data)

    '''
        envCell的生长函数
    '''
    def live(self):
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
