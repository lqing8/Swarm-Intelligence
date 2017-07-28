import sys,random
import pygame

'''
    规则要简单

    环境
        1:总体规则
        1.1:引入时间（统一的时钟频率）和生长周期（暂时没有定义）
        1.2:位置（统一的位置属性）
        1.3:统一的能量单位
        1.4:整数值，消除不定因素

    环境元素
        每一次update运算：
        1:生长属性:环境元素能量将变化，生长期+1能量,衰亡期-5能量
                    生长值上下极限能量范围100～2550，遇上而衰，遇下而生
        2:与细胞元素作用留下的信息属性被重置为0

    组织
        1:总体规则
        （暂时没有定义）

    组织细胞（cell）
        每一次update运算:
        1:生长属性：细胞会消耗能量10，能量少于100,休眠或死亡
                    而通过吸收环境元素能量维持自己的生存，细胞生命能量最大值2550
        2:能量行为：吸收细胞周边相邻各环境元素能量10/每个,与自己重合的环境元素能量20/每个，超出2550的多余能量会被存储，能量存储值暂未定义上限
        3:信息行为：改变细胞周边相邻各环境元素信息量10/每个，与自己重合的环境元素信息量10/每个
        3:运动属性：每一步移动耗能80，细胞不能重合
                    尽量少运动，减少能量损耗，如果需要移动的位置指向细胞自己，不动
                    向可能获取最大能量的单元移动，首选信息密度大于10的单元（因为可以从周边细胞一次性获取满格能量），其次向能量最多的环境元素移动

    ##  2017年7月28日，完成上述基本程序体设计
    ##  任务1：    寻找特定目标位置，并聚集


'''

class worldenv:

    def __init__(self, width, height):

        self.width, self.height = width, height
        self.size = 10
        self.envcells = []
        self.background = pygame.Surface((self.width * self.size, self.height * self.size))
        self.background.fill((20, 20, 20))

    def update(self):
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

    def findAround(self,grid):
        minW, minH, maxW, maxH = 1, 1, self.width, self.height

        if grid['x'] > minW:
            minW = grid['x'] - 1
        if grid['x'] < maxW:
            maxW = grid['x'] + 1

        if grid['y'] > minH:
            minH = grid['y'] - 1
        if grid['y'] < maxH:
            maxH = grid['y'] + 1

        around = []
        for x in range(minW, maxW + 1):
            for y in range(minH, maxH + 1):
                around.append({'x': x, 'y': y})

        return around

    def getID(self, grid):
        return self.height * (grid['x'] - 1) + grid['y'] - 1

class envCell:
        '''
        Init cell: size,eng and shape
        '''
        def __init__(self,size, id):
            self.id = id
            self.size = size
            self.growStep = 1
            self.eng = random.uniform(100, 2000) #最大值2550

            # -----------------------------------------------------
            # 可以设置环境元素的能量布局，布局不同，细胞会表现出不同行为特征
            if self.id < 2550:
                self.eng = self.id #random.uniform(100, 2000)
            if self.id >= 2550:
                self.eng = 2550 #random.uniform(100, 2000)
            # -----------------------------------------------------

            self.grid = {}
            self.shape = pygame.Surface((self.size - 2, self.size - 2))
            self.color = (0, int(self.eng/self.size), 0)
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
            #self.color = (self.color[0], self.eng, self.color[2])  # 这会一直保留细胞留下的信息量，并逐渐累计
            self.color = (0, int(self.eng/self.size), 0)    # 重置细胞留下的信息量为0
            self.shape.fill(self.color)

class vCells:

    def __init__(self, count, width, height):
        self.width, self.height = width, height
        self.count = count  #组织初始化时的细胞个数
        self.size = 10      #组织细胞的尺寸
        self.cells = []

    def update(self, env):
        screen = pygame.display.get_surface()

        n = 0
        while n < self.count:
            if len(self.cells) < self.count:
                self.cells.append(vCell(self.size, n))

                # -------------------------------------------------------
                # 设置细胞在环境中的布局，运行结果发现，对细胞群体行为没有什么影响
                self.cells[n].grid = {'x':random.randint(1,self.width),'y':random.randint(1,self.height)}
                #self.cells[n].grid = {'x':random.randint(1,20),'y':random.randint(1,20)}
                # -------------------------------------------------------
            else:
                self.cells[n].grow(env)
                self.cells[n].shareEng(env,self.cells)
                self.cells[n].goinEnv(env,self.cells)

            screen.blit(self.cells[n].shape,
                        (((self.cells[n].grid['x'] -1) * self.size), ((self.cells[n].grid['y'] -1) * self.size)))

            n = n + 1

class vCell:
        '''
        Init cell: size,eng and shape
        '''
        def __init__(self,size,id):
            self.id = id
            self.isLive = True
            self.liveStep = 10
            self.goStep = 80
            self.size = size
            self.eng = 2000 # random.uniform(100, 2500) #设置cell的初始能量，生命值，对群体行为没有什么影响
            self.dump_eng = 0
            self.grid = {}
            self.shape = pygame.Surface((self.size - 2, self.size - 2))
            self.color = (int(self.eng/self.size), 0, 0)
            self.shape.fill(self.color)

        def grow(self,env):
            self.eng = self.eng - self.liveStep
            if self.eng < 100: # 细胞死亡能量值为100
                self.isLive = False
                self.eng = 100
                self.color = (int(self.eng/self.size), 0, 255)
                self.shape.fill(self.color)
            else:
                #从环境中获得能量以延续生命，能量不息，生命不止
                self.eng = self.eng + self.getEngfromEnv(env)
                # 把缓存的能量首先供给自己
                self.eng = self.eng + self.dump_eng
                if self.eng > 2550:
                    self.dump_eng = self.eng - 2550
                    self.eng = 2550
                else:
                    self.dump_eng = 0
                #print(str(self.eng) + "******" + str(self.dump_eng))

                # ---------------------------------------------------
                # 标记存储在细胞缓存的能量级别大小
                if self.dump_eng > 50000:
                    self.color = (int(self.eng / self.size), 200, 0)
                elif self.dump_eng > 100000:
                    self.color = (int(self.eng / self.size), 200, 200)
                else:
                    self.color = (int(self.eng/self.size), 0, 0)
                # ---------------------------------------------------

                self.shape.fill(self.color)

        def getEngfromEnv(self, env):
            grids = env.findAround(self.grid)
            eng = 0
            for x in range(len(grids)):
                e = env.envcells[env.getID(grids[x])]
                r = e.color[0]
                b = e.color[2] * self.size  # cell对环境的信息量，表现在环境颜色的blue属性上

                if e.eng >= 100 + self.liveStep:    # 环境元素能量在最低标准之上，可以吸取能量
                    if e.grid == self.grid:
                        # 与细胞重合的中心环境元素能量吸收加倍，信息量不加倍
                        e.eng = e.eng - self.liveStep * 2
                        eng = eng + self.liveStep * 2
                        b = b + self.liveStep * 1
                    else:
                        #细胞周边的环境元素能量、信息量按常规吸收
                        e.eng = e.eng - self.liveStep
                        eng = eng + self.liveStep
                        b = b + self.liveStep * 1

                if b >= 2550:
                    b = 2550
                e.color = (r,int(e.eng/self.size),int(b/self.size))
                e.shape.fill(e.color)
            return eng

        def shareEng(self,env,cells):
            if self.dump_eng > 0:
                grids = env.findAround(self.grid)
                grids.remove(self.grid)

                # 1.找出周边的细胞，把多余能量给他们
                for x in range(len(cells)):
                    if self.dump_eng == 0: break
                    for y in range(len(grids)):
                        if self.dump_eng == 0: break
                        if cells[x].grid == grids[y]:
                            cells[x].eng = cells[x].eng + self.dump_eng
                            if cells[x].eng > 2550:
                                self.dump_eng = cells[x].eng - 2550
                                cells[x].eng = 2550
                            else:
                                self.dump_eng = 0
                            #print(str(cells[x].id) + ":" + str(cells[x].eng) + "******" + str(self.dump_eng))
                            break

        #细胞向周边环境元素移动
        def goinEnv(self,env,cells):
            if self.eng >= 1000 + self.goStep: #有足够的能量，大于109,才能行走
                grids = env.findAround(self.grid)

                #1.细胞不能重合,去掉与细胞重合的grid数组元素
                for x in range(len(cells)):
                    for y in range(len(grids)):
                        if cells[x].grid == grids[y]:
                            del grids[y]
                            break
                #2.增加自己，可能会不移动，降低活跃度，节省能量
                grids.append(self.grid)

                if len(grids) > 0:
                    g1,g2 = grids[0],grids[0]
                    eid = env.getID(g1)
                    eng = env.envcells[eid].eng
                    info = env.envcells[eid].color[2] * self.size

                    # 得到能量最多的环境元素位置
                    for x in range(1, len(grids)):
                        g_1 = grids[x]
                        eid_1 = env.getID(g_1)
                        if env.envcells[eid_1].eng > eng:
                            eng = env.envcells[eid_1].eng
                            g1 = g_1
                        #print(str(self.id) + ":" + str(env.envcells[eid_1].eng) + str("===") + str(eng) + "---" + str(x))

                    # 得到信息密度最大的环境元素位置
                    for x in range(1, len(grids)):
                        g_1 = grids[x]
                        eid_1 = env.getID(g_1)
                        if env.envcells[eid_1].color[2] * self.size > info:
                            info = env.envcells[eid_1].color[2] * self.size
                            g2 = g_1
                        #print(
                        #    str(self.id) + ":" + str(env.envcells[eid_1].color[2] * self.size) + str("===") + str(info) + "---" + str(x))

                    # 细胞与环境元素重合，则不移动，否则移动并损耗自身能量
                    if info > 10:   #信息优先，info>10说明周边有同类，优先移动到信息量最大，聚集密度最高的位置
                        if self.grid != g2:
                            self.grid = g2
                            self.eng = self.eng - self.goStep
                    else:
                        if self.grid != g1:
                            self.grid = g1
                            self.eng = self.eng - self.goStep

pygame.init()
pygame.display.set_mode((600,600))
pygame.display.set_caption("Hello World!")
clock = pygame.time.Clock()
clock.tick(60)

bg = worldenv(60,60)
cs = vCells(120,60,60)

bg.update()
cs.update(bg)

pygame.display.flip()
#pygame.time.wait(50000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    bg.update()
    cs.update(bg)

    pygame.display.flip()
    #pygame.time.wait(300)