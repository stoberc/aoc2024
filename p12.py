from aoc_utils import DIRECTIONS4

FNAME = "in12.txt"

# load input
grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

part1 = 0
part2 = 0
handled = set() # logs any locations that have already been processed
# loop through all locations
for x in range(width):
    for y in range(height):
        # if we stumble upon a previously undiscovered region...
        if (x, y) not in handled:
            # explore it
            expandq = [(x, y)] # queue of locations to check for neighbors
            region = set() # this will hold the set of all coordinates which are members
            v = grid[y][x] # the label associated with this region
            while expandq:
                sx, sy = expandq.pop()
                region.add((sx, sy))
                for dx, dy in DIRECTIONS4:
                    nx, ny = sx + dx, sy + dy
                    if (nx, ny) not in region and 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == v:
                        expandq.append((nx, ny))
            area = len(region)
            
            # find all edges
            # an edge is represented as a coordinate and a direction you could go from there to cross an edge
            # (x, y, dx, dy)
            edges = []
            for sx, sy in region:
                for dx, dy in DIRECTIONS4:
                    nx, ny = sx + dx, sy + dy
                    if nx < 0 or nx >= width or ny < 0 or ny >= height or grid[ny][nx] != v:
                        edges.append((sx, sy, dx, dy))
                    
            # goal: count exactly one edge from each side
            edge_leaders = set() # the set of those chosen edges
            edge_followers = set() # the set of all other edges
            for edge in edges:
                # if this edge has already been dominated by another, move on
                if edge in edge_followers:
                    continue
                # must be the leader of an unprocessed edge; log it
                edge_leaders.add(edge)
                nx, ny, dx, dy = edge
                
                # expand outwards from this edge, 
                # pushing any valid neighbors into the followers category
                for ddx, ddy in DIRECTIONS4:
                    bddx, bddy = ddx, ddy
                    while (nx + ddx, ny + ddy, dx, dy) in edges:
                        edge_followers.add((nx + ddx, ny + ddy, dx, dy))
                        ddx += bddx
                        ddy += bddy
                             
            part1 += area * len(edges)
            part2 += area * len(edge_leaders)
            handled |= region

print("Part 1:", part1)
print("Part 2:", part2)
