class Vertex:
    '''
    Vertex类，即演员的类
    '''
    def __init__(self, name):
        self.name = name  # 演员姓名
        self.connectedTo = {}  # 与之相关的演员列表以及对应参演的电影
        self.movieList = []  # 参演电影列表
        self.color = 'white'

        self.dist = 0  # 距离参数
        self.pred = None
        self.disc = 0
        self.fin = 0

    def __hash__(self):
        '''
        定义hash特殊方法来使得Vertex可以作为字典的key
        '''
        return hash(self.getName())
    
    def __str__(self):
        return str(self.name) + ":color " + self.color + ":disc " + \
               str(self.disc) + ":fin " + str(self.fin) + ":dist " + \
               str(self.dist) + ":pred \n\t[" + str(self.pred)+ "]\n"

    # def __lt__(self,o):
    #     return self.name < o.id
    def addNeighbor(self, nbr, edge, movie_id: str):
        '''
        以演员作为key来存储共同出演的movie列表。
        '''
        self.connectedTo[nbr] = edge
        self.addParticipateMovie(movie_id)
        
    def addParticipateMovie(self, movie_id: str):
        '''
        将该电影加入参演过的电影列表中
        '''
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

    def setDiscovery(self, dtime):
        self.disc = dtime
        
    def setFinish(self, ftime):
        self.fin = ftime
    
    def getFinish(self):
        return self.fin
        
    def getDiscovery(self):
        return self.disc
        
    def getPred(self):
        return self.pred
        
    def getDistance(self):
        return self.dist
        
    def getColor(self):
        return self.color
    
    def getConnections(self):
        return self.connectedTo.keys()
    
    def getName(self):
        return self.name
    
    def getParticipateMoviesID(self):
        '''
        用于返回参与过的电影的列表
        :return: list
        '''
        return self.movieList
    
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
        self.vertices = {} # 用来存储所有的演员（顶点）
        self.movies = {} # 用来存储所有的电影id以及对应的信息
        self.coMovies = {} # 用来存储某两个演员之间共事过的电影（边）
        self.numVertices = 0
        
    def __contains__(self, n):
        return n in self.vertices
        
    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex
        return newVertex
    
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
        for actorA in actors:
            for actorB in actors:
                if actorA != actorB:
                    self.addEdge(actorA, actorB, movie_id) # 添加A和B之间的连结
    
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
    
    def getCoMovieNames(self, actorA: str, actorB: str):
        '''
        获得两人参演的所有电影名
        :return: str array
        '''
        co_actors = (min(actorA, actorB), max(actorA, actorB))
        if co_actors in self.coMovies:
            idList = self.coMovies[co_actors].getAllMovieID()
            return list(map(lambda x: self.movies[x], idList))
        
    def getAverageStar(self, actor):
        '''
        给出输入的演员拍摄电影的平均星级
        '''
        actor_vertex = self.vertices[actor]
        movie_list = actor_vertex.getParticipateMoviesID()
        n = actor_vertex.getNumMovies()
        return sum(map(lambda x: self.movies[x]["star"], movie_list)) / n

    def getMovieTypesRank(self, actor):
        '''
        给出所有电影类型的排名及其出现次数
        :return: set array
        '''
        actor_vertex = self.vertices[actor]
        movie_list = actor_vertex.getParticipateMoviesID()
        types = {}  # 用于统计不同电影类型的数目
        
        for movie_id in movie_list:
            for movie_type in self.movies[movie_id]["type"]:
                if movie_type not in types:
                    types[movie_type] = 1
                else:
                    types[movie_type] += 1
        
        typesArray = []  # 电影类型列表，用于排序
        for movie_type, num in types.items():
            typesArray.append((movie_type, num))
        
        return sorted(typesArray, key=lambda x: x[1], reverse=True) # 从高到底排列
    
    def getVertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None
    
    def getVertices(self):
        return list(self.vertices.keys())
        
    def __iter__(self):
        return iter(self.vertices.values())

import json
if __name__ == '__main__':
    f = open('Film.json', encoding='utf-8')
    G = Graph()
    data = json.load(f)
    for item in data:
        G.addData(item)
        
    typeRank = G.getMovieTypesRank("周星驰")
    for t in typeRank:
        print(t)