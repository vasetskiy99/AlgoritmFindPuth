import json
from collections import deque

import numpy


class CommandsForFindObstacle(object):
    def __init__(self, grid):
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1]  # , [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.grid = grid
        self.grid_by_print = []
        self.cols = len(grid[0])
        self.rows = len(grid)
        self.start = (0, 0)
        self.goal = (10, 5)
        self.queue = deque([self.start])
        self.visited = {}
        self.path = []
        self.direction = []

        # self._get_start()
        self._completion_graph()

    def find_path(self):
        self._find_short_path()

    def _find_short_path(self):
        self._bfs()
        self._get_path()
        self.start = self.goal
        self.grid[self.goal[1]][self.goal[0]] = 0

    def _get_start(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == 3:
                    self.start = (x, y)
                    self.grid[y][x] = 0

    def _check_next_node(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows and (self.grid[y][x] == 0 or self.grid[y][x] == 2):
            return True
        else:
            return False

    def _get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if self._check_next_node(x + dx, y + dy)]

    def _bfs(self):
        queue = deque([self.start])
        visited = {self.start: None}

        while queue:
            cur_node = queue.popleft()
            if self.grid[cur_node[1]][cur_node[0]] == 2:
                self.goal = cur_node
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
                if col == 2 or col == 0:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self._get_next_nodes(x, y)

    def _get_path(self):
        path_head = self.goal
        self.path = []
        while path_head in self.visited:
            self.path.append(path_head)
            path_head = self.visited[path_head]
        self.path.reverse()

    def print_path(self):
        self.grid_by_print = json.loads(json.dumps(self.grid, separators=(',', ':')))
        for point in self.path:
            self.grid_by_print[point[1]][point[0]] = 9
            if point == self.goal:
                self.grid_by_print[point[1]][point[0]] = 2
            if point == self.start:
                self.grid_by_print[point[1]][point[0]] = 3

        for y, row in enumerate(self.grid_by_print):
            row_str = ""
            for x, col in enumerate(row):
                row_str += str(col) + "   "
            print(row_str)

    def file_write_path(self):
        f = open('path.txt', 'w')
        self.grid_by_print = numpy.copy(self.grid)

        for point in self.path:
            self.grid_by_print[point[1]][point[0]] = 9
            if point == self.goal:
                self.grid_by_print[point[1]][point[0]] = 2
            if point == self.start:
                self.grid_by_print[point[1]][point[0]] = 3

        for y, row in enumerate(self.grid_by_print):
            row_str = ""
            for x, col in enumerate(row):
                row_str += str(col) + "   "
            f.write(row_str + '\n')

    def prepare_path(self):
        angle = []
        for i in range(len(self.path) - 2):
            if (self.path[i][0] != self.path[i + 2][0]) and (self.path[i][1] != self.path[i + 2][1]):
                angle.append(self.path[i + 1])
        return angle
