from aoc_utils import UP, DOWN, LEFT, RIGHT

FNAME = "in6.txt"
    
# load the map
grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

# find the starting guard location
for y in range(height):
    if '^' in grid[y]:
        gy = y
        gx = grid[y].index('^')

sgx, sgy = gx, gy # cache the starting location
direction = UP

def turn_right(d):
    if d == UP:
        return RIGHT
    elif d == RIGHT:
        return DOWN
    elif d == DOWN:
        return LEFT
    else:
        return UP
    
# log for visited locations
visited = set()
visited.add((gx, gy))

# until we're out of bounds, proceed, turning right when obstacle encountered
while 0 <= gx < width and 0 <= gy < height:
    dx, dy = direction
    nx, ny = gx + dx, gy + dy
    if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == '#':
        direction = turn_right(direction)
    else:
        gx, gy = nx, ny
        visited.add((gx, gy))
        
print("Part 1:", len(visited) - 1) # don't count the final location

# loop through every possible open space, try putting an obstacle there,
# and see what happens
# inefficient but workable
part2 = 0
for x in range(width):
    for y in range(height):
        
        # insert obstacle
        if grid[y][x] in '#^':
            continue
        assert grid[y][x] == '.'
        grid[y][x] = '#'
        
        # reset the guard and log
        gx, gy = sgx, sgy
        direction = UP
        visited = set()
        visited.add((gx, gy, direction))
        
        # proceed until out of bounds or looped
        while 0 <= gx < width and 0 <= gy < height:
            
            # figure out the next location (in front of guard)
            dx, dy = direction
            nx, ny = gx + dx, gy + dy
            
            # if it's an obstacle, turn right and log it
            if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == '#':
                direction = turn_right(direction)
                visited.add((gx, gy, direction))
            else:
                # step forward
                gx, gy = nx, ny
                
                # if we've been here before, that's a loop
                if (gx, gy, direction) in visited:
                    part2 += 1
                    break
                else:
                    visited.add((gx, gy, direction))
        
        # clear the trial the obstacle
        grid[y][x] = '.'
               
print("Part 2:", part2);
