from aoc_utils import DIRECTIONS4
import re

FNAME = "in18.txt"

# grid is fixed at 71x71 with start at top left, end at bottom right
HEIGHT = 71
WIDTH = 71
SX, SY = 0, 0
EX, EY = 70, 70
    
def parse_line(line):
    return [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers
bytes = [parse_line(line) for line in open(FNAME).read().splitlines()]

# keep track of where obstacles are--just the first 1024 at first
obstacles = set()
for x, y in bytes[:1024]:
    obstacles.add((x, y))
    
# simple BFS ought to do it
distances = {(SX, SY): 0}
expandq = [(SX, SY)]
while expandq:
    x, y = expandq.pop(0)
    for dx, dy in DIRECTIONS4:
        nx, ny = x + dx, y + dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in obstacles and (nx, ny) not in distances:
            distances[(nx, ny)] = distances[(x, y)] + 1
            expandq.append((nx, ny))
print("Part 1:", distances[(EX, EY)])

# there's probably a clever and more efficient way to do this,
# but brute force shouldn't be too bad
# just add obstacles in one at a time, running BFS all over again
for ox, oy in bytes[1024:]:
    obstacles.add((ox, oy))
    distances = {(SX, SY): 0}
    expandq = [(SX, SY)]
    while expandq:
        x, y = expandq.pop(0)
        for dx, dy in DIRECTIONS4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in obstacles and (nx, ny) not in distances:
                distances[(nx, ny)] = distances[(x, y)] + 1
                expandq.append((nx, ny))
    if (EX, EY) not in distances:
        break
print(f"Part 2: {ox},{oy}")
