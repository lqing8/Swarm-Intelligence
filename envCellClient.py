# coding:utf8
import json
import sys,random
import time
import pygame
from socket import *

class envCell:
    '''
    Init envCell
    '''
    def __init__(self, initData):
        self.id = 1                     #envCell 的唯一标识符ID
        self.size = 10                  #正方形图形大小尺寸，default 10
        self.clock = 1000               #时钟频率（毫秒）
        self.energyStep = 1             #能量单元
        self.coordinate = {'x':1,'y':1}    #在环境中的位置坐标

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

        self.stringToData(initData)     #server初始化每一个envCell

        self.color = (0, int(self.energy / self.size), 0)  #将能量通过green color显示出来
        # 绘制envCell
        self.shape = pygame.Surface((self.size - 2, self.size - 2))
        self.shape.fill(self.color)

    '''
        环境会改变每个envCell的能量值
    '''
    def setEnergy(self, energy):
        self.energy = energy

    '''
        把envCell的所有信息输出
    '''
    def dataToString(self):
        dt = {};
        dt['id'] = self.id
        dt['size'] = self.size
        dt['clock'] = self.clock
        dt['coordinate'] = self.coordinate
        dt['energy'] = self.energy

        return json.dumps(dt)

    '''
        环境对envCell的所有信息进行重置
    '''
    def stringToData(self,str):
        try:
            dt = json.loads(str)
            if dt.get('id') != None: self.id = dt['id']
            if dt.get('size') != None: self.size = dt['size']
            if dt.get('clock') != None: self.clock = dt['clock']
            if dt.get('coordinate') != None: self.coordinate = dt['coordinate']
            if dt.get('energy') != None: self.energy = dt['energy']

        except Exception as e:
            print(e)

    '''
        envCell内部，生物钟控制的生长函数
    '''
    def liveWithClock(self):
        # 环境元素能量将变化，生长期+1能量,衰亡期-5能量；生长值上下极限能量范围100～2550，遇上而衰，遇下而生。
        if self.energy <= 100:
            self.energyStep = 1
        if self.energy >= 2550:
            self.energyStep = -5
        self.energy = self.energy + self.energyStep
        time.sleep(self.clock / 1000)

        ########   以下为记忆功能   ########
        # self.color = (0, int(self.eng/self.size), 0)    # 重置细胞留下的信息量为0
        #b = self.color[2] - 3
        #if b < 0: b = 0
        #if b > 250: b = 250
        #self.color = (self.color[0], int(self.eng / self.size), b)  # 这会一直保留细胞留下的信息量，并逐渐累计
        #self.shape.fill(self.color)

    '''
        嵌入到环境中，和服务器通讯（infomation receive and send）
    '''
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

ec = envCell('{"size": 10, "id": 10, "energy": 2001, "clock": 3000, "coordinate": {"x": 10, "y": 10}}')
ec.liveWithClock()
print(ec.dataToString())
