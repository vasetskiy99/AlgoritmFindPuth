import CommandsForFindObstacle
import numpy as np

grid = np.load('./result.npy')

# grid = [
#     [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
#     [0, 2, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 2, 1, 0],
#     [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 1, 0],
# ]

commands = CommandsForFindObstacle.CommandsForFindObstacle(grid)
commands.find_path()
commands.file_write_path()
print(commands.path)
print(commands.prepare_path())

commands.find_path()
# commands.print_path()
print(commands.path)

commands.find_path()
# print(commands.path)
# commands.print_path()
