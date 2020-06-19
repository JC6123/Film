import json
import matplotlib as plt
from graph import *
import sys

sys.setrecursionlimit(10 ** 7)  # 设置最大递归深度
# 但是仅仅设置递归深度不够，需要栈空间配合
# threading线程模块可以设定线程的栈空间
import threading

threading.stack_size(2 ** 27)  # 把线程的栈空间提上去


def bfs(g: Graph):
    branches = []
    for vertex in g.getActorList():
        if vertex.getColor() == 'white':
            branches.append(_bfs(vertex, []))
        
    return branches


def _bfs(actor: Vertex, branch: list):
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
        _bfs(temp_actor, branch)
        
    return branch


def myProg1():
    G = Graph()
    
    f =open('Film.json',encoding='utf-8')  # 加载数据
    data = json.load(f)
    for item in data:
        G.addData(item)
        
    branches = bfs(G)
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
    
    branches = bfs(G)
    branches.sort(key=lambda x: (len(x), x), reverse=True)
    
    
def myProg3():
    G = Graph()
    
    f = open('Film.json', encoding='utf-8')  # 加载数据
    data = json.load(f)
    for item in data:
        G.addData(item)
    
    branches = bfs(G)
    branches.sort(key=lambda x: (len(x), x), reverse=True)


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
    
        
# 把程序主要功能定义为一个函数
# 开一个线程来执行这个函数，这样就拥有设定的栈空间
t = threading.Thread(target=myProg45)
t.start()  # 启动线程
t.join()  # 进程等待线程结束