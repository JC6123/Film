# 演员的小世界

<center>成昱璇 1700012145

## 图的基本结构和构建

定义了`Vertex`、`Edge`、`Graph`三个类。其中`Vertex`用于存储演员的有关信息，`Edge`用于存储两个演员共事过的电影，`Graph`用于存储所有演员以及共事的信息。

构建`Graph`时，利用`addData`将读入的电影数据以电影ID为键，存储在`self.movies`字典中。同时调用`addEdge`以及`addVertex`创建演员连接关系和演员结点。如果一部电影没有演员，则不存储；如果只有一位演员，则创建一条连接自身的边。

## Q1

#### 连通分支

定义了函数`bfs`，采用BFS算法对`Graph`中的所有演员节点进行遍历，将每个连通分支以列表形式存储，并将所有联通分支作为列表储存。

构建了辅助函数`_bfs`用于递归过程。利用`Vertex`中定义的属性`color`，用于表示“是否搜索过”。

连通分支数目即为`bfs`返回列表的长度；每个连通分支演员数目即为子列表的长度。主进程和结果如下：

![image-20200619130652801](C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200619130652801.png)

![image-20200619130719444](C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200619130719444.png)

#### 参演电影类型

在`Graph`中定义了`getMovieTypesRank`方法，传入需要计算的演员名字列表。对每个演员参演过电影的ID集合取并集，并利用`self.movies`字典得到ID对应的电影信息，来统计电影的类型数目，最后返回排序后的元组列表，其中每个元组的第一项为电影类型，第二项为该类型的数目。

![image-20200619133231688](C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200619133231688.png)

<img src="C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200619132935649.png" alt="image-20200619132935649" style="zoom: 80%;" />

<img src="C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200619132954867.png" alt="image-20200619132954867" style="zoom:80%;" />

## Q2

连通分支的直径也可以用BFS算法来实现。调用了`calDistance`函数用来计算每个连通分支中的任意路径中的最大值。而辅助函数`bfsDist`则是用于计算以某位演员为起点的连通分支的路径长度。注意每调用一次`bfsDist`之后，要将该连通分支中的所有`Vertex`的`dist`属性重置为-1。

主进程如下：

![image-20200620113424897](C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200620113424897.png)

![image-20200620113407183](C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200620113407183.png)

## Q3

在Q1和Q2中得到所有连通分支后，利用`matplotlib.pyplot`中的工具可以将连通分支规模、直径大小、以及电影平均星级计算出来。其中计算平均星级时调用了`Graph`中的`getAverageStar`方法。

![Num](E:\Git\Film\Num.png)

![Diameter](E:\Git\Film\Diameter.png)

## Q4~Q5

`Graph`中定义了方法`getActor`用于获取该演员的`Vertex`，再利用`getCoActorNames`获取合作演员列表，并将其分别作为`Graph`中`getTheirMovieIDs`、`getAverageStar`和`getMovieTypesRank`方法的输入，就可以得到最终结果。

![image-20200619134457746](C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200619134457746.png)

![image-20200620114223040](C:\Users\17000\AppData\Roaming\Typora\typora-user-images\image-20200620114223040.png)

## Q6

