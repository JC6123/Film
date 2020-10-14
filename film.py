import json
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import sys

sys.setrecursionlimit(10 ** 7)  # 设置最大递归深度
# 但是仅仅设置递归深度不够，需要栈空间配合
# threading线程模块可以设定线程的栈空间
import threading

threading.stack_size(2 ** 27)  # 把线程的栈空间提上去


class Vertex:
    '''
    Vertex类，即演员的类
    '''
    def __init__(self, name):
        self.name = name  # 演员姓名
        self.connectedTo = {}  # 与之相关的演员列表以及对应参演的电影
        self.movieList = []  # 参演电影列表
        self.color = 'white'
        
        self.dist = -1  # 距离参数
        self.pred = None
    
    def addNeighbor(self, nbr, edge, movie_id: str):
        '''
        以演员作为key来存储共同出演的movie列表。
        '''
        self.connectedTo[nbr] = edge
        if movie_id not in self.movieList:
            self.movieList.append(movie_id)
    
    def isConnectedTo(self, nbr):
        '''
        判断是否和某演员有连结
        '''
        return True if nbr in self.connectedTo else False
    
    def setColor(self, color):
        self.color = color
    
    def setDistance(self, d):
        self.dist = d
    
    def setPred(self, p):
        self.pred = p
    
    def getDistance(self):
        return self.dist
    
    def getColor(self):
        return self.color
    
    def getPred(self):
        return self.pred
    
    def getName(self):
        '''
        该演员的名字
        :return: str
        '''
        return self.name
    
    def getConnections(self):
        '''
        返回所有有关演员列表
        :return: Vertex array
        '''
        return self.connectedTo.keys()
    
    def getParticipateMoviesID(self):
        '''
        用于返回参与过的电影的列表
        :return: list
        '''
        return self.movieList
    
    def getCoActorNames(self):
        '''
        返回所有共事演员的名字列表
        :return: str array
        '''
        return list(map(lambda x: x.getName(), self.connectedTo.keys()))
    
    def getNumMovies(self):
        '''
        用于返回参与电影的数目
        :return: int
        '''
        return len(self.movieList)


class Edge:
    def __init__(self):
        self.weight = 1
        self.movieList = []
    
    def addCoMovie(self, movie_id):
        self.movieList.append(movie_id)
    
    def getAllMovieID(self):
        return self.movieList


class Graph:
    def __init__(self):
        self.vertices = {}  # 用来存储所有的演员名字-vertex键值对（顶点）
        self.movies = {}  # 用来存储所有的电影id以及对应的信息
        self.coMovies = {}  # 用来存储某两个演员之间共事过的电影（边）
        self.numVertices = 0
    
    def __contains__(self, n):
        return n in self.vertices
    
    def addData(self, item: dict):
        '''
        向Graph中添加json文件中读入的字典数据
        '''
        movie_id = item["_id"]["$oid"]
        self.movies[movie_id] = {}
        self.movies[movie_id]["title"] = item["title"]
        self.movies[movie_id]["year"] = item["year"]
        self.movies[movie_id]["type"] = list(item["type"].split(","))
        self.movies[movie_id]["star"] = item["star"]
        self.movies[movie_id]["director"] = item["director"]
        self.movies[movie_id]["pp"] = item["pp"]
        self.movies[movie_id]["time"] = item["time"]
        self.movies[movie_id]["film_page"] = item["film_page"]
        
        actors = list(item["actor"].split(","))
        if actors != [""]:
            if len(actors) >= 2:
                for actorA in actors:
                    for actorB in actors:
                        if actorA != actorB:
                            self.addEdge(actorA, actorB, movie_id)  # 添加A和B之间的连结
            else:  # 只有一个演员，就自己跟自己连通
                actor = actors[0]
                if actor not in self.vertices:
                    self.addVertex(actor)
                edge = Edge()
                edge.addCoMovie(movie_id)
                self.vertices[actor].addNeighbor(self.vertices[actor],
                                                 edge, movie_id)
    
    def addEdge(self, actorA: str, actorB: str, movie_id: str):
        '''
        给actorA和actorB增加连结，并且更新共同出演电影的总表
        '''
        if actorA not in self.vertices:
            self.addVertex(actorA)
        if actorB not in self.vertices:
            self.addVertex(actorB)
        
        co_actors = (min(actorA, actorB), max(actorA, actorB))
        if co_actors not in self.coMovies:
            self.coMovies[co_actors] = Edge()
        self.coMovies[co_actors].addCoMovie(movie_id)
        
        self.vertices[actorA].addNeighbor(self.vertices[actorB],
                                          self.coMovies[co_actors], movie_id)
        self.vertices[actorB].addNeighbor(self.vertices[actorA],
                                          self.coMovies[co_actors], movie_id)
    
    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex
        return newVertex
    
    def getActor(self, name):
        '''
        获得演员名字对应的Vertex对象
        :return: Vertex
        '''
        return self.vertices[name]
    
    def getActorNames(self):
        '''
        获得所有演员名字列表
        :return: str array
        '''
        return self.vertices.keys()
    
    def getActorList(self):
        '''
        获得所有演员列表
        :return: Vertex array
        '''
        return self.vertices.values()
    
    def getTheirRelations(self, actorA: str, actorB: str):
        '''
        用于判断两者是否有连接。若有，则输出二者之间的一条可能的连接关系。
        '''
        if (actorA not in self.vertices.keys() or
                actorB not in self.vertices.keys()):
            print("Actor's name wrong")
            return
        if actorA != actorB:
            print("{} and {}".format(actorA, actorB))
            start = self.getActor(actorB)
            find = False
            start.setDistance(0)
            vertQueue = []
            vertQueue.append(start)
            while (len(vertQueue) > 0):
                currentVert = vertQueue.pop(0)
                for nbr in currentVert.getConnections():
                    if (nbr.getDistance() == -1):
                        nbr.setDistance(currentVert.getDistance() + 1)
                        nbr.setPred(currentVert)
                        if nbr.getName() == actorA:
                            find = True
                        vertQueue.append(nbr)
            
            if find:
                currentVert = self.getActor(actorA)
                print(currentVert.getName())
                while (currentVert.getName() != actorB):
                    actor1 = currentVert.getName()
                    actor2 = currentVert.getPred().getName()
                    print(" -> " + actor2 + ": " + "、".join(
                        i for i in self.getCoMovieNames(actor1, actor2)))
                    currentVert = currentVert.getPred()
            else:
                print("No connections between these two actors.")
        
        else:
            print("They are the same.")
    
    def getCoMovieNames(self, actorA: str, actorB: str):
        '''
        获得两人共同参演的所有电影名
        :return: str array
        '''
        co_actors = (min(actorA, actorB), max(actorA, actorB))
        if co_actors in self.coMovies:
            idList = self.coMovies[co_actors].getAllMovieID()
            return list(map(lambda x: self.movies[x]["title"], idList))
    
    def getAverageStar(self, actors):
        '''
        给出输入的演员拍摄电影的平均星级
        :param actors: str array / str
        :return: double
        '''
        movieList = self.getTheirMovieIDs(actors)
        n = len(movieList)
        return round(
            sum(map(lambda x: self.movies[x]["star"], movieList)) / n, 2)
    
    def getMovieTypesRank(self, actors: list):
        '''
        给出这些演员参演的所有电影类型的排名及其出现次数
        :param actor: str array / str
        :return: set array
        '''
        types = {}  # 用于统计不同电影类型的数目
        movieList = self.getTheirMovieIDs(actors)
        for movie_id in movieList:
            for movie_type in self.movies[movie_id]["type"]:
                if movie_type not in types:
                    types[movie_type] = 1
                else:
                    types[movie_type] += 1
        
        typesArray = []  # 电影类型列表，用于排序
        for movie_type, num in types.items():
            typesArray.append((movie_type, num))
        
        return sorted(typesArray, key=lambda x: x[1], reverse=True)  # 从高到底排列
    
    def getTheirMovieIDs(self, actors):
        '''
        给出这些演员参演的所有电影
        :param actors: str / str array
        :return: str array
        '''
        if isinstance(actors, str):
            actors = [actors]
        
        movieList = set()
        for actor in actors:
            actor_vertex = self.vertices[actor]
            movieList = movieList.union(set(
                actor_vertex.getParticipateMoviesID()))
        
        return movieList
    
    def getVertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None
    
    def getVertices(self):
        return list(self.vertices.keys())
    
    def __iter__(self):
        return iter(self.vertices.values())


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
    
    f = open('Film.json', encoding='utf-8')  # 加载数据
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
    
    name_list = list(range(1, 21)) + list(
        range(len(branches) - 19, len(branches) + 1))
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
t = threading.Thread(target=myProg45)
t.start()  # 启动线程
t.join()  # 进程等待线程结束