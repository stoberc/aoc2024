from collections import defaultdict

FNAME = "in8.txt"

grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

# create a list of coordinates for each antenna type
antennas = defaultdict(list)

# check whether coords are within limits
def inbounds(x, y):
    return 0 <= x < width and 0 <= y < height

# loop through the input, logging the coordinates of each antenna
for x in range(width):
    for y in range(height):
        if grid[y][x] != '.':
            antennas[grid[y][x]].append((x, y))

# find the antinodes of each antenna by projecting the differential distance
# past each antenna
def antis(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    p0 = (x1 + dx, y1 + dy)
    p1 = (x0 - dx, y0 - dy)
    results = []
    if inbounds(*p0):
        results.append(p0)
    if inbounds(*p1):
        results.append(p1)
    return results
    
# find the set of all points with antinodes by pairwise comparison
def count_antinodes():
    antinodes = set()
    for a in antennas:
        # there's probably some itertools function to write this more cleanly
        for i in range(len(antennas[a])):
            for j in range (i + 1, len(antennas[a])):
                antinodes.update(antis(*antennas[a][i], *antennas[a][j]))
    return len(antinodes)
                
print("Part 1:", count_antinodes())

# broader redefinition of antinodes for Part 2
def antis(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    results = []
    x, y = x1, y1
    while inbounds(x, y):
        results.append((x, y))
        x += dx
        y += dy
    x, y = x0, y0
    while inbounds(x, y):
        results.append((x, y))
        x -= dx
        y -= dy        
    return results
                
print("Part 2:", count_antinodes())
