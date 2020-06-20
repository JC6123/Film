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
        self.vertices = {} # 用来存储所有的演员名字-vertex键值对（顶点）
        self.movies = {} # 用来存储所有的电影id以及对应的信息
        self.coMovies = {} # 用来存储某两个演员之间共事过的电影（边）
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
    
    def getCoMovieNames(self, actorA: str, actorB: str):
        '''
        获得两人共同参演的所有电影名
        :return: str array
        '''
        co_actors = (min(actorA, actorB), max(actorA, actorB))
        if co_actors in self.coMovies:
            idList = self.coMovies[co_actors].getAllMovieID()
            return list(map(lambda x: self.movies[x], idList))
        
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
        
        return sorted(typesArray, key=lambda x: x[1], reverse=True) # 从高到底排列
    
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


import json
if __name__ == '__main__':
    f = open('Film.json', encoding='utf-8')
    G = Graph()
    data = json.load(f)
    for item in data:
        G.addData(item)
    
    print("周星驰出演电影的平均星级 " + str(G.getAverageStar("周星驰")))
    
    zxc = G.getActor("周星驰")
    co_actors = zxc.getCoActorNames()
    print("Number of actors: " + str(len(co_actors) + 1))  # 加1是包括了周星驰自己
    print("Number of movies: " + str(len(G.getTheirMovieIDs(co_actors))))
    print("Average stars: " + str(G.getAverageStar(co_actors)))
    print("Top 3 types: ")
    print("\n".join(map(str, G.getMovieTypesRank(co_actors)[0:3])))