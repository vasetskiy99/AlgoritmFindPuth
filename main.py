import CommandsForFindObstacle
import numpy as np

# grid = np.load('./result.npy')

grid = [
    [0, 1, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 1, 0],
]
path = [(4, 0), (4, 1), (3, 1), (2, 1), (2, 2), (2, 3), (2, 4), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (0, 8),
        (0, 9)]
commands = CommandsForFindObstacle.CommandsForFindObstacle(grid)
for i in range(len(commands.goals)):
    commands.find_path()
    commands.prepare_path(path)
    # commands.print_path()
