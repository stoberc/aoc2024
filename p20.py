from aoc_utils import DIRECTIONS4

FNAME = "in20.txt"

# load the map
grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

# find the start and end
for x in range(width):
    for y in range(height):
        if grid[y][x] == 'S':
            sx, sy = x, y
            grid[y][x] = '.'
        elif grid[y][x] == 'E':
            ex, ey = x, y
            grid[y][x] = '.'
            
# BFS find the distance of all nodes from the start
expandq = [(sx, sy)]
distances = {(sx, sy): 0}
while expandq:
    x, y = expandq.pop(0)
    for dx, dy in DIRECTIONS4:
        nx, ny = x + dx, y + dy
        if grid[ny][nx] == '.' and (nx, ny) not in distances:
            distances[(nx, ny)] = distances[(x, y)] + 1
            expandq.append((nx, ny))
distances_from_s = distances

# convenient for reasoning to also have the distance of all nodes from the end
distances_from_e = {}
for k in distances:
    distances_from_e[k] = distances[(ex, ey)] - distances[k]

# part 1: find all locations where a two-hop cheat would be really useful
part1 = 0            
for x, y in distances_from_s:
    for dx, dy in DIRECTIONS4:
        nx, ny = x + 2 * dx, y + 2 * dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == '.' and distances_from_s[(x, y)] + distances_from_e[(nx, ny)] + 2 <= distances_from_s[(ex, ey)] - 100:
            part1 += 1
print("Part 1:", part1)

# part 2: 20 hops now
# too annoying with dx/dy approach, 
# so instead just loop over the entire grid to see which points
# are worthy and legal cheat options
part2 = 0
for x, y in distances_from_s:
    for nx, ny in distances_from_s:
        if grid[ny][nx] == '.' and abs(nx - x) + abs(ny - y) <= 20 and distances_from_s[(x, y)] + distances_from_e[(nx, ny)] + abs(nx - x) + abs(ny - y) <= distances_from_s[(ex, ey)] - 100:
            part2 += 1
print("Part 2:", part2)
