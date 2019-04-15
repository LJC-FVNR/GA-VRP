import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random


# 获取区间长度
def getlength(accuracy=5, interval=(-1,1)):
    parts = (interval[1] - interval[0]) * (10 ** accuracy)
    for i in range(0, 100):
        if 2 ** i > parts:
            l = i
            break
        elif i == 99:
            print("Error on length")
    return l


# 二进制码转十进制数字
def decipher(bina, accuracy=5, interval=(-1,1)):
    length = getlength(accuracy=accuracy, interval=interval)
    pin = int(str(bina), 2)
    code = interval[0] + pin*((interval[1]-interval[0])/((2**length)-1))
    return code


# 初始种群
def init_pop(scale, length):
    seed = ['0', '1']
    initpop = []
    for i in range(0, scale):
        temp = ''
        for j in range(0, length):
            temp = temp + random.choice(seed)
        initpop.append(temp)
    return initpop


# 种群解码
def decipherpop(pop, accuracy, interval):
    decipherpop = []
    for i in pop:
        decipherpop.append(
            decipher(i, accuracy, interval)
        )
    return decipherpop

# 适应度函数
def fity(x):
    y = x*np.sin(10*np.pi*x)+2
    return y

# 计算解码后种群适应度
def fitness(decipherpop):
    fit = []
    for i in decipherpop:
        fit.append(fity(i))
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


# 轮盘赌选择生成新种群
def new_pop(lastbinpop, fit):
    fit = np.array(fit)
    scale = lastbinpop.__len__()
    fit_p = mean(fit, 1)        # 取到的概率
    pop = []
    bestarg = np.argwhere(fit == fit.max())[0][0]
    pop.append(lastbinpop[bestarg])
    for i in range(1, scale):
        temp = np.random.choice(lastbinpop, p=fit_p.ravel())
        pop.append(temp)
    return pop


def bestcode(pop, fit):
    arg = np.where(fit == fit.max())[0][0]
    return pop[arg]


def cross(x1, x2):
    temp1 = x1
    temp2 = x2
    length = x1.__len__()
    point = np.random.choice(range(0, length - 1))
    templeft = ['', '']
    for j in range(0, point + 1):
        templeft[0] = str(templeft[0]) + str(temp1[j])
        templeft[1] = str(templeft[1]) + str(temp2[j])
    tempright = ['', '']
    for k in range(point + 1, length):
        tempright[0] = str(tempright[0]) + str(temp1[k])
        tempright[1] = str(tempright[1]) + str(temp2[k])
    temp3 = str(templeft[0]) + str(tempright[1])
    temp4 = str(templeft[1]) + str(tempright[0])
    return temp3, temp4


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
    return list(pop)

# 变异
def mutation(pop, possibility):
    scale = pop.__len__()
    length = pop[0].__len__()
    quant = round(scale*length*possibility)
    pop = np.array(pop)
    for i in range(quant):
        arg = np.random.choice(range(scale))
        seri = pop[arg]
        p = []
        for i in seri:
            p.append(i)
        p = np.array(p)
        point = np.random.choice(range(0, length))
        if seri[point] == '0':
            p[point] = 1
        else:
            p[point] = 0
        o = ''
        for i in p:
            o = o + i
        pop[arg] = o
    return list(pop)


class GA:
    def __init__(self, scale, accuracy, interval, times, crossP, mutationP):
        self.scale = scale
        self.accuracy = accuracy
        self.interval = interval
        self.length = getlength(accuracy=accuracy, interval=interval)
        self.times = times
        self.gen = []
        self.bestfit = []
        self.bestcode = []
        self.bestX = []
        self.crossP = crossP
        self.mutationP = mutationP
        self.currentpop = []


    def process(self):
        pop = init_pop(self.scale, self.length)
        for i in range(self.times):
            self.gen.append(i)
            dp = decipherpop(pop, self.accuracy, self.interval)
            fit = fitness(dp)
            self.bestfit.append(fit.max())
            self.bestcode.append(bestcode(pop, fit))
            bestX = decipher(bestcode(pop,fit), self.accuracy, self.interval)
            self.bestX.append(bestX)
            pop = new_pop(pop, fit)
            pop = cross_pop(pop, self.crossP)
            pop = mutation(pop, self.mutationP)
        self.currentpop = pop
        return fit.max()


    def drawFit(self):
        plt.plot(self.gen, self.bestfit)
        plt.show()
    def drawX(self):
        plt.plot(self.gen, self.bestX)
        plt.show()
    def drawY(self):
        x = np.linspace(self.interval[0], self.interval[1], 1000)
        y = fity(x)
        plt.plot(x,y)
        plt.plot(self.bestX[-1], self.bestfit[-1], 'o')
        plt.show()


if __name__ == "__main__":
    ga = GA(60, 5, (-1, 2), 300, 0.25, 0.01)
    ga.process()
    ga.drawFit()
    ga.drawX()
    ga.drawY()
