import json
from graph import *


G = Graph()

f =open('Film.json',encoding='utf-8')  # 加载数据
data = json.load(f)
for item in data:
    G.addData(item)
    
