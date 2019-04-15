import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

# 顺序表
def sheet(cLabel):
    cLabel = np.array(cLabel)
    n = cLabel.shape[0]
    sheet = np.array(range(1, n+1))
    return sheet

# 顺序编码转旅程
def decipher(queue, sheet):
    tour = []
    sheet = np.array(sheet)
    l = sheet.shape[0]
    for i in range(l):
        tour.append(sheet[queue[i]-1])
        sheet = np.delete(sheet, queue[i]-1)
    return tour

# 旅程转顺序编码
def cipher(tour, sheet):
    queue = []
    l = sheet.shape[0]
    for i in range(l):
        arg = np.argwhere(sheet == tour[i])[0][0] + 1
        queue.append(arg)
        sheet = np.delete(sheet, arg-1)
    return queue

# 初始种群
def init_pop(scale, sheet):
    initpop = []
    for i in range(0, scale):
        temptour = np.random.permutation(sheet)
        initpop.append(cipher(temptour, sheet))
    return initpop

# 旅程转全程
def Full(tour, cX, cY, cD, dX, dY, dLabel, origin):
    D = []
    for i in tour:
        D.append(cD[i-1])
    full = []
    full.append(origin)
    temp = '/'
    for i in range(0, D.__len__()):
        if D[i] is temp:
            pass
        else:
            dx = dX[np.argwhere(dLabel == D[i])[0][0]]
            dy = dY[np.argwhere(dLabel == D[i])[0][0]]
            dpos = [dx, dy]
            full.append(dpos)
        cx = cX[tour[i]-1]
        cy = cY[tour[i]-1]
        cpos = [cx, cy]
        full.append(cpos)
        temp = D[i]
    return full

def element(tour,cD):
    D = []
    for i in tour:
        D.append(cD[i-1])
    Element = []
    temp = '/'
    for i in range(0, D.__len__()):
        if D[i] is temp:
            pass
        else:
            Element.append(D[i])
        Element.append(tour[i])
        temp = D[i]
    return Element

# 种群解码
def decipherpop(popq, sheet):
    decipherpop = []
    for i in popq:
        decipherpop.append(
            decipher(i, sheet)
        )
    return decipherpop

# 种群编码
def cipherpop(popt, sheet):
    cipherpop = []
    for i in popt:
        cipherpop.append(
            cipher(i, sheet)
        )
    return cipherpop

# 距离
def getdistance(a,b):
    d = np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return d

def tourdistance(position):
    l = position.__len__()
    d = 0
    for i in zip(range(l-1), range(1, l)):
        axy = [position[i[0]][0], position[i[0]][1]]
        bxy = [position[i[1]][0], position[i[1]][1]]
        d = d + getdistance(axy, bxy)
    return d

# 适应度函数__待扩展
def fity(position):
    y = -tourdistance(position)
    return y

# 计算解码后种群适应度
def fitness(decipherpop, cX, cY, cD, dX, dY, dLabel, origin):
    fit = []
    for i in decipherpop:
        path = Full(i, cX, cY, cD, dX, dY, dLabel, origin)
        fit.append(fity(path))
    fit = np.array(fit)
    return fit

# 归一化
def mean(x, direction):
    if direction == "+" or direction == 1:
        x = np.array(x)
    if direction == "-" or direction == -1:
        x = 1/np.array(x)
    y = x/x.sum()
    return y

# 轮盘赌生成新种群
def new_pop(lastbinpop, fit):
    fit = np.array(fit)
    scale = lastbinpop.__len__()
    fit_p = mean(fit, 1)        # 取到的概率
    pop = []
    bestarg = np.argwhere(fit == fit.max())[0][0]
    arga, argb, argc = np.argsort(fit)[-1], np.argsort(fit)[-2], np.argsort(fit)[-3]
    pop.append(lastbinpop[arga])
    pop.append(lastbinpop[arga])
    pop.append(lastbinpop[argb])
    pop.append(lastbinpop[argc])
    for i in range(5, scale):
        arg = np.random.choice(range(0, fit.shape[0]), p=fit_p.ravel())
        pop.append(lastbinpop[arg])
    return pop


def bestcode(pop, fit):
    arg = np.where(fit == fit.max())[0][0]
    return pop[arg]


def cross(x1, x2):
    temp1 = x1
    temp2 = x2
    length = x1.__len__()
    point = np.random.choice(range(0, length - 1))
    templeft = [[], []]
    for j in range(0, point + 1):
        templeft[0].append(temp1[j])
        templeft[1].append(temp2[j])
    tempright = [[], []]
    for k in range(point + 1, length):
        tempright[0].append(temp1[k])
        tempright[1].append(temp2[k])
    L1 = templeft[0]
    L2 = templeft[1]
    R1 = tempright[1]
    R2 = tempright[0]
    L1.extend(R1)
    L2.extend(R2)
    return L1, L2


# 交叉
def cross_pop(pop, possibility):
    scale = pop.__len__()
    length = pop[0].__len__()
    group = round((scale/2)*possibility)*2
    temp_pop = pop
    cr = []
    arg = []
    tabu = []
    for i in range(group):
        n = np.random.choice(range(scale))
        while n in tabu:
            n = np.random.choice(range(scale))
        tabu.append(n)
        arg.append(n)
        nn = pop[n]
        cr.append(nn)
    gr = np.array(range(group)).reshape(round(group/2), 2)
    for i in range(round(group/2)):
        a, b = cross(cr[gr[i][0]], cr[gr[i][1]])
        cr[gr[i][0]] = a
        cr[gr[i][1]] = b
    arg = np.array(arg)
    cr = np.array(cr)
    pop = np.array(pop)
    for i in range(group):
        q = cr[i]
        ar = arg[i]
        pop[ar] = q
    return pop

# 变异
def mutation(pop, possibility, sheet):
    scale = pop.__len__()
    length = pop[0].__len__()
    quant = round(scale*length*possibility)
    poporigin = decipherpop(pop, sheet)
    popd = np.array(poporigin)
    for i in range(quant):
        arg = np.random.choice(range(scale))
        mut1 = np.random.choice(range(length))
        mut2 = np.random.choice(range(length))
        temp1 = popd[arg][mut1]
        temp2 = popd[arg][mut2]
        popd[arg][mut1] = temp2
        popd[arg][mut2] = temp1
    out = cipherpop(popd, sheet)
    return out


class GA:
    def __init__(self, scale, times, crossP, mutationP, cLabel, cX, cY, cD, dLabel, dX, dY, origin):
        self.scale = scale
        self.sheet = sheet(cLabel)
        self.cLabel = cLabel
        self.times = times
        self.origin = origin
        self.gen = []
        self.bestfit = []
        self.bestcode = []
        self.crossP = crossP
        self.mutationP = mutationP
        self.currentpop = []
        self.cX = cX
        self.cY = cY
        self.cD = cD
        self.dLabel = dLabel
        self.dX = dX
        self.dY = dY
    def process(self):
        pop = init_pop(self.scale, self.sheet)      # 编码后
        for i in range(self.times):
            self.gen.append(i)
            dp = decipherpop(pop, self.sheet)       # 解码
            fit = fitness(dp, self.cX, self.cY, self.cD, self.dX, self.dY, self.dLabel, self.origin)      # 适应度
            self.bestfit.append(fit.max())
            self.bestcode.append(bestcode(dp, fit))
            pop = new_pop(pop, fit)                 # 编码后
            pop = cross_pop(pop, self.crossP)       # 交叉
            pop = mutation(pop, self.mutationP, self.sheet)     # 变异
        self.currentpop = pop
        return fit.max()
    def drawgen(self):
        plt.plot(self.gen,self.bestfit)
        plt.savefig('./static/images/drawgen.jpg')
        plt.show()
    def drawbestline(self):
        path = Full(self.bestcode[-1], self.cX, self.cY, self.cD, self.dX, self.dY, self.dLabel, self.origin)
        l = path.__len__()
        plt.plot(self.cX, self.cY, 'o')
        plt.plot(self.dX, self.dY, 'o')
        plt.plot(self.origin[0], self.origin[1], 'o')
        for i in range(self.cX.shape[0]):
            plt.text(self.cX[i], self.cY[i], self.cLabel[i], family='serif', ha='right', wrap=True)
            plt.text(self.cX[i], self.cY[i] + 0.5, 'Demand:' + self.cD[i], family='serif', ha='right', wrap=True)
        for i in range(self.dX.shape[0]):
            plt.text(self.dX[i], self.dY[i], self.dLabel[i], family='serif', ha='right', wrap=True)
        for i in zip(range(l - 1), range(1, l)):
            x1 = path[i[0]][0]
            x2 = path[i[1]][0]
            y1 = path[i[0]][1]
            y2 = path[i[1]][1]
            plt.plot([x1, x2], [y1, y2])
        plt.savefig('./static/images/drawbestline.jpg')
        plt.show()


if __name__ == "__main__":
    customer = pd.read_csv('Customer.csv')
    distribution = pd.read_csv("Distribution.csv")
    cLabel = np.array(customer.iloc[:, 0])
    cX = np.array(customer.iloc[:, 1])
    cY = np.array(customer.iloc[:, 2])
    cD = np.array(customer.iloc[:, 3])
    dLabel = np.array(distribution.iloc[:, 0])
    dX = np.array(distribution.iloc[:, 1])
    dY = np.array(distribution.iloc[:, 2])
    origin = (1, 1)
    plt.plot(cX, cY, 'o')
    plt.plot(dX, dY, 'o')
    plt.plot(1, 1, 'o')
    for i in range(cX.shape[0]):
        plt.text(cX[i], cY[i], cLabel[i], family='serif', ha='right', wrap=True)
        plt.text(cX[i], cY[i]+0.5, 'Demand:'+cD[i], family='serif', ha='right', wrap=True)
    for i in range(dX.shape[0]):
        plt.text(dX[i], dY[i], dLabel[i], family='serif', ha='right', wrap=True)
    plt.show()

    tsp = GA(100, 500, 0.25, 0.02, cLabel, cX, cY, cD, dLabel, dX, dY, (1, 1))
    tsp.process()
    tsp.drawgen()
    tsp.drawbestline()

