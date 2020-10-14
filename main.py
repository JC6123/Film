import json
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from graph import *
import sys

sys.setrecursionlimit(10 ** 7)  # 设置最大递归深度
# 但是仅仅设置递归深度不够，需要栈空间配合
# threading线程模块可以设定线程的栈空间
import threading

threading.stack_size(2 ** 27)  # 把线程的栈空间提上去


def bfsBranches(g: Graph):
    branches = []
    for vertex in g.getActorList():
        if vertex.getColor() == 'white':
            branches.append(_bfsBranches(vertex, []))
        
    return branches


def _bfsBranches(actor: Vertex, branch: list):
    temp = []
    
    if actor.getColor() == 'white':
        actor.setColor('black')
        branch.append(actor.getName())
        
    coList = actor.getConnections()
    for co_actor in coList:
        if co_actor.getColor() == 'white':
            branch.append(co_actor.getName())
            co_actor.setColor('black')
            temp.append(co_actor)
    
    for temp_actor in temp:
        _bfsBranches(temp_actor, branch)
        
    return branch


def calDistance(G: Graph, actors: list):
    dist = 0
    for name in actors:
        actor = G.getActor(name)
        dist = max(dist, bfsDist(actor))
        for name1 in actors:  # 对遍历过演员的dist参数进行重置
            actor1 = G.getActor(name1)
            actor1.setDistance(-1)
    return dist


def bfsDist(start: Vertex):
    dist = 0
    start.setDistance(0)
    vertQueue = []
    vertQueue.append(start)
    while (len(vertQueue) > 0):
        currentVert = vertQueue.pop(0)
        for nbr in currentVert.getConnections():
            if (nbr.getDistance() == -1):
                nbr.setDistance(currentVert.getDistance() + 1)
                vertQueue.append(nbr)
        dist = currentVert.getDistance()
    return dist


def myProg1():
    G = Graph()
    
    f =open('Film.json',encoding='utf-8')  # 加载数据
    data = json.load(f)
    for item in data:
        G.addData(item)
        
    branches = bfsBranches(G)
    branches.sort(key=lambda x: (len(x), x), reverse=True)
    
    print("总连通分支数")
    print(len(branches))
    print("前20个连通分支大小")
    print('、'.join(str(len(branch)) for branch in branches[0:20]))
    print("后20个连通分支大小")
    print('、'.join(str(len(branch)) for branch in branches[-21:-1]))
    
    print("前20个连通分支中top3的电影类型")
    for branch in branches[0:20]:
        typeRank = G.getMovieTypesRank(branch)
        print('、'.join(str(t[0]) for t in typeRank[0:min(3, len(typeRank))]))
    print("后20个连通分支中top3的电影类型")
    for branch in branches[-21:-1]:
        typeRank = G.getMovieTypesRank(branch)
        print('、'.join(str(t[0]) for t in typeRank[0:min(3, len(typeRank))]))
        
      
def myProg2():
    G = Graph()
    
    f = open('Film.json', encoding='utf-8')  # 加载数据
    data = json.load(f)
    for item in data:
        G.addData(item)
    
    branches = bfsBranches(G)
    branches.sort(key=lambda x: (len(x), x), reverse=True)
    
    print("前20个连通分支直径")
    print("-1、" + "、".join(str(calDistance(G, branch))
                          for branch in branches[1:20]))
    print("后20个连通分支直径")
    print("、".join(str(calDistance(G, branch)) for branch in branches[-21:-1]))
    
    
def myProg3():
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    G = Graph()
    
    f = open('Film.json', encoding='utf-8')  # 加载数据
    data = json.load(f)
    for item in data:
        G.addData(item)
    
    branches = bfsBranches(G)
    branches.sort(key=lambda x: (len(x), x), reverse=True)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height,
                     '%s' % float(height))

    name_list = list(range(1, 21)) + list(range(len(branches)-19, len(branches)+1))
    num_list = list(map(lambda x: len(x), branches[0:20] + branches[-21:-1]))
    plt.figure(1)
    autolabel(plt.bar(range(len(num_list)), num_list, color='b',
                      tick_label=name_list))
    plt.yscale('symlog')
    plt.xlabel(u"连通分支大小排名", fontproperties=font_set)
    plt.ylabel(u"连通分支数量（对数坐标）", fontproperties=font_set)
    plt.title(u"连通分支规模表", fontproperties=font_set)
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    fig.savefig('Num.png', dpi=100)

    plt.figure(2)
    num_list = list(map(lambda x: G.getAverageStar(x),
                        branches[0:20] + branches[-21:-1]))
    autolabel(plt.bar(range(len(num_list)), num_list, color='b',
                      tick_label=name_list))
    plt.xlabel(u"连通分支大小排名", fontproperties=font_set)
    plt.ylabel(u"电影的平均星级", fontproperties=font_set)
    plt.title(u"电影平均星级表", fontproperties=font_set)
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    fig.savefig('Star.png', dpi=100)
    
    plt.figure(3)
    num_list = [-1] + list(map(lambda x: calDistance(G, x),
                               branches[1:20] + branches[-21:-1]))
    autolabel(plt.bar(range(len(num_list)), num_list, color='b',
                      tick_label=name_list))
    plt.xlabel(u"连通分支大小排名", fontproperties=font_set)
    plt.ylabel(u"连通分支直径", fontproperties=font_set)
    plt.title(u"连通分支直径表", fontproperties=font_set)
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    fig.savefig('Diameter.png', dpi=100)


def myProg45():
    G = Graph()
    
    f = open('Film.json', encoding='utf-8')  # 加载数据
    data = json.load(f)
    for item in data:
        G.addData(item)

    print("周星驰出演电影的平均星级: " + str(G.getAverageStar("周星驰")))
    
    zxc = G.getActor("周星驰")
    co_actors = zxc.getCoActorNames()
    print("周星驰及其共同出演者")
    print("Number of actors: " + str(len(co_actors) + 1))  # 加1是包括了周星驰自己
    print("Number of movies: " + str(len(G.getTheirMovieIDs(co_actors))))
    print("Average stars: " + str(G.getAverageStar(co_actors)))
    print("Top 3 types: ")
    print("\n".join(map(str, G.getMovieTypesRank(co_actors)[0:3])))


def myProg6():
    G = Graph()
    
    f = open('Film.json', encoding='utf-8')  # 加载数据
    data = json.load(f)
    for item in data:
        G.addData(item)
        
    G.getTheirRelations("周星驰", "汤姆·克鲁斯")
    
        
# 把程序主要功能定义为一个函数
# 开一个线程来执行这个函数，这样就拥有设定的栈空间
t = threading.Thread(target=myProg1)
t.start()  # 启动线程
t.join()  # 进程等待线程结束