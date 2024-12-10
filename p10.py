from aoc_utils import DIRECTIONS4

FNAME = "in10.txt"

grid = [[int(i) for i in list(line)] for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

# returns a set of summits reachable from this place
# could be some value in memoizing this, since multiple paths wind over each other
# but performance is fine, so not bothering
def reachable_summits(x, y):
    
    v = grid[y][x]
    
    # if we're at a summit...
    if v == 9:
        return set([(x, y)])
    
    # find all the summits reachable from neighboring positions 
    # as long as their value is one more than this one
    rs = set()
    for dx, dy in DIRECTIONS4:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == v + 1:
            rs |= reachable_summits(nx, ny)
    return rs
 
# find all trailheads and accumulate their scores
part1 = 0 
for x in range(width):
    for y in range(height):
        if grid[y][x] == 0:
            part1 += len(reachable_summits(x, y))
print("Part 1:", part1)

# returns the number of paths from here to a summit
# could be some value in memoizing this, since multiple paths wind over each other
# but performance is fine, so not bothering
def rating(x, y):
    v = grid[y][x]
    
    # if we're at the summit, one path ends here
    if v == 9:
        return 1
        
    # accumlate the number of paths from all valid neighbors
    total = 0
    for dx, dy in DIRECTIONS4:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == v + 1:
            total += rating(nx, ny)
    return total
 
# find all trailheads and accumulate their ratings 
part2 = 0 
for x in range(width):
    for y in range(height):
        if grid[y][x] == 0:
            part2 += rating(x, y) 
print("Part 2:", part2)
