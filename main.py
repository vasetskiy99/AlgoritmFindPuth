import CommandsForFindObstacle
import numpy as np

grid = np.load('./result.npy')

# grid = [
#     [0, 1, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
#     [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
#     [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
#     [2, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 0],
# ]

commands = CommandsForFindObstacle.CommandsForFindObstacle(grid)
commands.find_path()
print(commands.path)
# commands.print_path()



# print(commands.get_directions())
# commands.print_path(goal=commands.goals[0])
# commands.file_write_path(goal=commands.goals[0])

# graph = {}
#
# cols, rows = len(grid[0]), len(grid)
# start = (0, 0)
# goal = (0, 0)
#
#
# def get_next_nodes(x, y):
#     def check_next_node(x, y):
#         if 0 <= x < cols and 0 <= y < rows and not grid[y][x]:
#             return True
#         else:
#             return False
#
#     ways = [-1, 0], [0, -1], [1, 0], [0, 1]  # , [-1, -1], [1, -1], [1, 1], [-1, 1]
#     result = [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]
#     return result
#
#
# def bfs(start, goal, graph):
#     queue = deque([start])
#     visited = {start: None}
#
#     while queue:
#         cur_node = queue.popleft()
#         if cur_node == goal:
#             break
#
#         next_nodes = graph[cur_node]
#         for next_node in next_nodes:
#             if next_node not in visited:
#                 queue.append(next_node)
#                 visited[next_node] = cur_node
#     return visited
#
#
# for y, row in enumerate(grid):
#     for x, col in enumerate(row):
#         if col == 3:
#             start = (x, y)
#             grid[y][x] = 0
#         if col == 2:
#             goal = (x, y)
#             grid[y][x] = 0
#
# for y, row in enumerate(grid):
#     for x, col in enumerate(row):
#         if not col:
#             graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)
#
# queue = deque([start])
# visited = bfs(start, goal, graph)
# path_head = goal
# path = []
#
# while path_head in visited:
#     path.append(path_head)
#     path_head = visited[path_head]
#
# path.reverse()
# print(path)
# for point in path:
#     grid[point[1]][point[0]] = "*"
#     if point == goal:
#         grid[point[1]][point[0]] = "2"
#     if point == start:
#         grid[point[1]][point[0]] = "3"
#
# for y, row in enumerate(grid):
#     rowStr = ""
#     for x, col in enumerate(row):
#         rowStr += str(col) + "      "
#     print(rowStr)
