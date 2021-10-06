# 15数码（15-puzzle）问题
- 学号：
- 姓名：
- 操作系统：macOS Big Sur 11.6
- 编译语言：python

## 问题介绍

## 问题形式化
**形式化棋盘位置**
```python
def loc_ele(state, element):
    # assert 0 <= element <= 15
    # # 要解决的15数码问题，其每个元素必然都非负且小于16
    x, y = "", ""
    # x和y的初位置都为空
    for i in range(len(state)):
        # i为行数
        try:
            x = state[i].index[element]
            y = i
        except ValueError:
            pass
    assert isinstance(x, int) and isinstance(y, int)
    # 判断x和y是否是整数类型
    return y, x
```

**定义棋盘的移动**
> 可以改进，看学姐的示范代码
```python
def move(state, direction):
    new_state = copy.deepcopy(state) #原状态深拷贝
    zero_y, zero_x = loc_ele(new_state, 0)
    if direction == "up":
        if zero_y > 0:
            new_state[zero_y][zero_x] = new_state[zero_y - 1][zero_x]
            new_state[zero_y -1][zero_x] = 0
        return new_state
    elif direction == "down":
        if zero_y < 3:
            new_state[zero_y][zero_x] = ew_state[zero_y + 1][zero_x]
            new_state[zero_y + 1][zero_x] = 0
        return new_state
    elif direction == "left":
        if zero_x > 1:
            new_state[zero_y][zero_x] = new_state[zero_y][zero_x - 1]
            new_state[zero_y][zero_x-1] = 0
        return new_state
    elif direction == "right":
        if zero_x <3:
            new_state[zero_y][zero_x] = new_state[zero_y][zero_x + 1]
            new_state[zero_y][zero_x + 1] = 0
        return new_state
    else:
        raise("invalid direction input in function move !")
```

## 无信息搜索（盲目搜索）：深度受限算法

## 有信息搜索：`A*`算法
