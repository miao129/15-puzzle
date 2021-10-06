import numpy as np
from copy import deepcopy
from utils import *

goal_state=[[1, 2, 3, 4], 
            [5, 6, 7, 8], 
            [9, 10, 11, 12], 
            [13, 14, 15, 0]]

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


class Node(object):  # Represents a node in a search tree
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        self.h = h(self.state)
        if parent:
            self.depth = parent.depth + 1

    def child_node(self, problem, action):
        next_state = problem.move(self.state, action)
        next_node = Node(next_state, self, action,
                         problem.g(self.path_cost, self.state,
                                   action, next_state))
        return next_node

    def path(self):
        """
        Returns list of nodes from this node to the root node
        """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __repr__(self):
        return "<Node {}(g={})>".format(self.state, self.path_cost)

    def __lt__(self, other):
        # return self.path_cost < other.path_cost
        return self.h < other.h

    def __eq__(self, other):
        return self.state == other.state


class Problem(object):
    def __init__(self, init_state=None, goal_state=None):
        self.init_state = Node(init_state)
        self.goal_state = Node(goal_state)

    def actions(self, state):
        """
        Given the current state, return valid actions.
        :param state:
        :return: valid actions
        """
        pass

    def move(self, state, action):
        pass

    def is_goal(self, state):
        pass

    def g(self, cost, from_state, action, to_state):
        return cost + 1

    def solution(self, goal):
        """
        Returns actions from this node to the root node
        """
        if goal.state is None:
            return None
        return [node.action for node in goal.path()[1:]]

    def expand(self, node):  # Returns a list of child nodes
        return [node.child_node(self, action) for action in self.actions(node.state)]
    

class GridsProblem(Problem):
    def __init__(self,
                 n,
                 init_state=[[11, 9, 4, 15], 
                             [1, 3, 0, 12], 
                             [7, 5, 8, 6], 
                             [13, 2, 10, 14]],
                 goal_state=[[1, 2, 3, 4], 
                             [5, 6, 7, 8], 
                             [9, 10, 11, 12], 
                             [13, 14, 15, 0]]):
        super().__init__(init_state, goal_state)
        self.n = n
        
    """
    # 报告中的示范题目
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
    """

    def is_valid(self, loc):
        if -1 < loc[0] < self.n and -1 < loc[1] < self.n:
            return True
        else:
            return False

    def actions(self, state):
        empty_row, empty_col = np.where(np.array(state) == 0)[0][0], np.where(np.array(state) == 0)[1][0]
        candidates = [[empty_row-1, empty_col], [empty_row+1, empty_col],
                      [empty_row, empty_col-1], [empty_row, empty_col+1]]
        valid_candidates = [item for item in candidates if self.is_valid(item)]
        return valid_candidates

    def move(self, state, action):
        empty_row, empty_col = np.where(np.array(state) == 0)[0][0], np.where(np.array(state) == 0)[1][0]
        new_state = deepcopy(state)
        new_state[empty_row][empty_col] = state[action[0]][action[1]]
        new_state[action[0]][action[1]] = 0
        return new_state

    def is_goal(self, state):
        return state == self.goal_state.state

    def g(self, cost, from_state, action, to_state):
        return cost + 1
    
def search_with_info(problem):
    # A*搜索
    
    node = problem.init_state
    open = PriorityQueue(node)
    closed = []

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


def search_without_info(problem):
    # 使用宽度优先搜索
    
    node = problem.init_state
    if problem.is_goal(node.state):
        return node, 1
    
    open = Queue()
    open.push(node)
    closed = []

    while not open.empty():
        node = open.pop()
        # closed.add(tuple(node))
        closed.append(node)
        # print(len(closed))

        for child in problem.expand(node):
            # if child.state not in open or closed._items:
            if child not in open._items and child not in closed:
                if problem.is_goal(child.state):
                    return child, len(closed)+1
                open.push(child)
    return None


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