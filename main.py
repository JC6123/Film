import json
from graph import *


def dfs(g: Graph):
    branches = []
    for vertex in g.getActorList():
        if vertex.isAlone():
            branches.append([vertex.getName()])
        elif vertex.getColor() == "white":
            branches.append(_dfs(vertex, []))
        
    return branches


def _dfs(actor: Vertex, branch: list):
    if actor.getColor() == "white":
        actor.setColor("gray")
        branch.append(actor.getName())
        has_any_white = "False"
        has_all_black = "True"
        
        for co_actor in actor.getConnections():
            if co_actor.getColor() == "white":  # 如果有一个白色就进入下一层搜索
                has_any_white = "True"
                has_all_black = "False"
                _dfs(co_actor, branch)
            elif co_actor.getColor() == "gray":  # 如果有灰色则说明不全黑
                has_all_black = "False"
                
        if not has_any_white:
            if has_all_black:
                return branch
            else:  # 表示共事演员没有白色但不全为黑，就继续探索
                _dfs(actor, branch)
                
    elif actor.getColor() == "gray" or actor.getColor() == "black":
        actor.setColor("black")
        has_all_black = "True"
        for co_actor in actor.getConnections():
            if co_actor.getColor() == "gray":
                _dfs(co_actor, branch)
        
        if has_all_black:
            return branch
        

G = Graph()

f =open('Film.json',encoding='utf-8')  # 加载数据
data = json.load(f)
counter = 0
for item in data:
    counter += 1
    G.addData(item)
    if counter > 500:
        break
    
branches = dfs(G)
for branch in branches:
    print(branch)