import json
from collections import deque


class CommandsForFindObstacle(object):
    def __init__(self, grid):
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1]  # , [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.grid = grid
        self.grid_by_print = []
        self.cols = len(grid[0])
        self.rows = len(grid)
        self.start = (0, 0)
        self.goal = (0, 0)
        self.goals = []
        self.queue = deque([self.start])
        self.visited = {}
        self.path = []
        self.direction = []
        self._get_start_and_goals()
        self._completion_graph()

    def find_path(self):
        # self._find_short_path()
        self._bfs(self.goals[1])
        self._get_path(self.goals[1])
        self._get_path(self.goals[0])
    # def _find_short_path(self):
    #     len_to_path = {}
    #     for i, el in enumerate(self.goals):
    #         self._bfs(goal=el)
    #         self._get_path(goal=el)
    #         len_to_path.update({el: len(self.path)})
    #     length_path = len_to_path.get(self.goals[0])
    #     for point in len_to_path.items():
    #         if length_path > point[1]:
    #             length_path = point[1]
    #             self.goal = point[0]
    #     self._bfs(goal=self.goal)
    #     self._get_path(goal=self.goal)
    #     self.start = self.goal
    #     # self.goals.remove(self.goal)
    #     for goal in self.goals:
    #         if goal == self.goal:
    #             self.goals.remove(self.goal)

    def _get_start_and_goals(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == 3:
                    self.start = (x, y)
                    self.grid[y][x] = 0
                if col == 2:
                    self.goals.append((x, y))
                    self.grid[y][x] = 0

    def _check_next_node(self, x, y):
        return True if 0 <= x < self.cols and 0 <= y < self.rows and not self.grid[y][x] else False

    def _get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if self._check_next_node(x + dx, y + dy)]

    def _bfs(self, goal):
        queue = deque([self.start])
        visited = {self.start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break

            next_nodes = self.graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        self.visited = visited

    def _completion_graph(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self._get_next_nodes(x, y)

    def _get_path(self, goal):
        path_head = goal
        while path_head in self.visited:
            self.path.append(path_head)
            path_head = self.visited[path_head]
        self.path.reverse()

    # def print_path(self):
    #     self.grid_by_print = json.loads(json.dumps(self.grid, separators=(',', ':')))
    #     for point in self.path:
    #         self.grid_by_print[point[1]][point[0]] = 9
    #         if point == self.goal:
    #             self.grid_by_print[point[1]][point[0]] = 2
    #         if point == self.start:
    #             self.grid_by_print[point[1]][point[0]] = 3

        for y, row in enumerate(self.grid_by_print):
            row_str = ""
            for x, col in enumerate(row):
                row_str += str(col) + "   "
            print(row_str)

    def file_write_path(self, goal):
        f = open('path.txt', 'w')
        for point in self.path:
            self.grid[point[1]][point[0]] = 9
            if point == goal:
                self.grid[point[1]][point[0]] = "2"
            if point == self.start:
                self.grid[point[1]][point[0]] = "3"

        for y, row in enumerate(self.grid):
            row_str = ""
            for x, col in enumerate(row):
                row_str += str(col) + "   "
            f.write(row_str + '\n')

    def get_directions(self):
        self.direction = []
        for i in range(len(self.path) - 1):
            xp, yp = self.path[i]
            xn, yn = self.path[i + 1]
            if xp == xn:
                if yp > yn:
                    self.direction.append('Up')
                else:
                    self.direction.append('Down')
            if yp == yn:
                if xp > xn:
                    self.direction.append('Left')
                else:
                    self.direction.append('Right')
        return self.direction
