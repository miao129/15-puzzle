# 15数码（15-puzzle）
- 姓名：Yang Miao
- 操作系统：macOS Big Sur 11.6
- 编译语言：python 3.8.8 64-bit（packages needed: numpy、collections、sortedcontainers）

## Honor Code
除`search_without_info`和`search_with_info`的函数定义，启发函数的定义外，主程序的运行外，其余变量定义内容（包括utils.py和problem.py中的内容皆来自助教Jiang Lan）

## 1. 问题介绍及作业要求

15数码问题是在4×4方格盘上，放有15个数码，剩下一个位置为空(方便起见，用0表示空)，每一空格其上下左右的数码可移至空格。本问题给定初始位置和目标位置，要求通过一系列的数码移动，将初始状态转化为目标状态(如下图所示)。
<img src="https://i.loli.net/2021/10/06/iZ1sEjCmrpaLkgK.png" alt="iZ1sEjCmrpaLkgK"  />

**作业要求**
1. 用一种无信息搜索方法编程求解；
2. 用一种有信息搜索方法编程求解；
3. 以上两种求解方法哪种更好?为什么?



## 2. 无信息搜索（盲目搜索）：宽度优先算法（BFS）

对于无信息搜索方法，我们选择实现宽度优先搜索，其伪代码为：

![USCBO1yQtdnDF5V](https://i.loli.net/2021/10/06/USCBO1yQtdnDF5V.jpg)

根据伪代码，写出的python代码实现为：

```python
def search_without_info(problem):
    # 使用宽度优先搜索
    
    node = problem.init_state
    if problem.is_goal(node.state):
        return node, 1
      # 若初始状态即为目标状态，则返回node，遍历数量为1
    
    open = Queue()
    # 用队列维护开节点表，其中Queue类型来自于utils文件中定义
    open.push(node)
    closed = []
    # 用python自带的set维护闭节点表

    while not open.empty():
        node = open.pop()
        closed.append(node)
   
        for child in problem.expand(node):
            if child not in open._items and child not in closed:
                if problem.is_goal(child.state):
                    return child, len(closed)+1
              			# 在生成节点时即检查
                open.push(child)
    return None
```



## 3. 有信息搜索：`A*`算法

对于有信息搜索，我们选择A*算法，其伪代码如下：

![dtTjbp5XKA68IYV](https://i.loli.net/2021/10/06/dtTjbp5XKA68IYV.jpg)

根据伪代码，写出的python代码实现为：

```python
def search_with_info(problem):
    # A*搜索
    
    node = problem.init_state
    open = PriorityQueue(node)
    # 用优先队列维护一个开节点表
    closed = []
    # 用python自带的集合维护一个闭节点表

    if problem.is_goal(node.state):
        return node, 1
    else:
        while not open.empty():
            node = open.pop()
            if problem.is_goal(node.state):
                return node, len(closed)+1
            closed.append(node)

            for child in problem.expand(node):
                if child not in open._queue and child not in closed:
                    open.push(child)
                elif child in open._queue:
                    idx = open._queue.index(child)
                    open.compare_and_replace(idx, child)
        return None
```

其中，我们用曼哈顿距离定义启发函数h：

```python
# 形式化element在state中的位置
def loc_ele(state, element):
    x, y = "", ""
    # x和y的初位置都为空
    for i in range(len(state)):
        # i为行数
        try:
            x = state[i].index(element)
            y = i
        except ValueError:
            pass
    assert isinstance(x, int) and isinstance(y, int)
    # 判断x和y是否是整数类型
    return y, x

# 用曼哈顿距离定义启发函数
def h(from_state, to_state = goal_state):
    h_cost = 0
    for i in range(16):
        init_y, init_x = loc_ele(from_state, i)
        goal_y, goal_x = loc_ele(to_state, i)
        h_cost += abs(init_y - goal_y) + abs(init_x - goal_x)
    return h_cost
```



## 4. 运行结果及方法比较

由于原题目对于笔记本来说需要的计算时间过长，于是我才用了一个简单一些的初始状态来进行计算（可以在problem.py文件的相应位置注释中找到）

```python
class GridsProblem(Problem):
  def __init__(self,
                 n,
                 init_state=[[1, 2, 8, 3], 
                             [5, 7, 10, 4], 
                             [9, 0, 11, 12], 
                             [13, 6, 14, 15]],
                 goal_state=[[1, 2, 3, 4], 
                             [5, 6, 7, 8], 
                             [9, 10, 11, 12], 
                             [13, 14, 15, 0]]):
        super().__init__(init_state, goal_state)
        self.n = n
```

对于该问题的求解，我们运行主程序：

```python
if __name__ == "__main__":
    problem = GridsProblem(4)
    
    goal_state, steps = search_with_info(problem)
    state = goal_state
    state_list = []
    action_list = []
    state_list.append(goal_state.state)
    action_list.append(goal_state.action)
    while(state.parent):
        state = state.parent
        state_list.append(state.state)
        action_list.append(state.action)
    state_list.reverse()
    action_list.reverse()
    print("for A* Search:")
    for i in range(len(action_list)-1):
        print(state_list[i])
        print("move",i+1,": " , action_list[i+1])
    print(state_list[-1])
    print("共遍历：",steps)
    
    print("\n")

    goal_state, steps = search_without_info(problem)
    state = goal_state
    state_list = []
    action_list = []
    state_list.append(goal_state.state)
    action_list.append(goal_state.action)
    while(state.parent):
        state = state.parent
        state_list.append(state.state)
        action_list.append(state.action)
    state_list.reverse()
    action_list.reverse()
    print("for BFS:")
    for i in range(len(action_list)-1):
        print(state_list[i])
        print("move",i+1,": ", action_list[i+1])
    print(state_list[-1])
    print("共遍历：",steps)
```

得到结果：

![NhUsGjLebSy2WJ5](https://i.loli.net/2021/10/06/NhUsGjLebSy2WJ5.png)

![nyZkBMqRfT2si3F](https://i.loli.net/2021/10/06/nyZkBMqRfT2si3F.png)

可以看出，`A*`算法只需要遍历27个节点即可找出问题求解的最优路径，而BFS需要遍历17387个节点才能找出最优路径，需要花费大量的时间和空间，效率远低于`A*`算法。

而在理论推导过程中，我们也可以得知，宽度优先算法的时间和空间复杂度都是指数级的，且分支因子很大；而`A*`算法的时间和空间复杂度虽然也是指数级的，但由于其分支因子一般较小，所以复杂度较低。

综上，我认为`A*`算法在时间和空间效率上更好。
