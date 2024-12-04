import pdb
from aoc_utils import *

FNAME = "in4.txt"

grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

count = 0

for x in range(0, width):
    for y in range(0, height):
        if grid[y][x] == 'X':
            for dx, dy in DIRECTIONS8:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 'M':
                    nx, ny = nx + dx, ny + dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 'A':
                        nx, ny = nx + dx, ny + dy
                        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 'S':
                            count += 1
print("Part1:", count)

count = 0
for x in range(0, width):
    for y in range(0, height):
        if grid[y][x] == 'A':
            subcount = 0
            for dx, dy in DIRECTIONS8:
                if (dx, dy) in DIRECTIONS4:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == 'M':
                    rx, ry = x - dx, y - dy
                    if 0 <= rx < width and 0 <= ry < height and grid[ry][rx] == 'S':
                        subcount += 1
            if subcount == 2:
                count += 1
            
print("Part2:", count)

pdb.set_trace()
