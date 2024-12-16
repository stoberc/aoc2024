from aoc_utils import turn_left, turn_right, turn_around, UP, DOWN, LEFT, RIGHT, DIRECTIONS4

FNAME = "in16.txt"

grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])
      
# identify start and end      
for x in range(width):
    for y in range(height):
        if grid[y][x] == 'S':
            sx, sy = x, y
            grid[y][x] = '.'
        elif grid[y][x] == 'E':
            ex, ey = x, y
            grid[y][x] = '.'
            
# ineffient Dijkstra's - no minheap, sort at each addition
# hopefully Python's sort is great on mostly sorted lists
expandq = [(0, sx, sy, RIGHT)]
distance = {} # the distance of each state from the starting state
while expandq: # useful for part2 if we expand until all states explored instead of terminating when end is found
    v, x, y, dir = expandq.pop(0)
    if (x, y, dir) in distance:
        continue
    distance[(x, y, dir)] = v
    dx, dy = dir

    # go forward for one point
    if grid[y + dy][x + dx] == '.' and (x + dx, y + dy, dir) not in distance:
        expandq.append((v + 1, x + dx, y + dy, dir))
        
    # turn for 1000 points
    ddx, ddy = turn_left(dir)
    if (x, y, (ddx, ddy)) not in distance:
        expandq.append((v + 1000, x, y, (ddx, ddy)))
    ddx, ddy = turn_right(dir)
    if (x, y, (ddx, ddy)) not in distance:
        expandq.append((v + 1000, x, y, (ddx, ddy)))
    
    expandq.sort() # make sure we're always expanding closest nodes first

part1 = min(distance[(ex, ey, dir)] for dir in DIRECTIONS4)
print("Part 1:", part1)

distance_from_s = distance # so far, we've found the distance from starting state to all states

# now we want to find the distance from E to all states
# which with a subsequent reversal will give the distance from all states to E
distance = {}
expandq = [(0, ex, ey, dir) for dir in DIRECTIONS4]
while expandq: # useful for part2 if we expand until all states explored instead of terminating when end is found
    v, x, y, dir = expandq.pop(0)
    if (x, y, dir) in distance:
        continue
    distance[(x, y, dir)] = v
    dx, dy = dir

    # go forward for one point
    if grid[y + dy][x + dx] == '.' and (x + dx, y + dy, dir) not in distance:
        expandq.append((v + 1, x + dx, y + dy, dir))
        
    # turn for 1000 points
    ddx, ddy = turn_left(dir)
    if (x, y, (ddx, ddy)) not in distance:
        expandq.append((v + 1000, x, y, (ddx, ddy)))
    ddx, ddy = turn_right(dir)
    if (x, y, (ddx, ddy)) not in distance:
        expandq.append((v + 1000, x, y, (ddx, ddy)))
    
    expandq.sort() # make sure we're always expanding closest nodes first

# perform the reversal
distance_from_e = distance
distance_to_e = {}
for x, y, dir in distance_from_e:
    v = distance_from_e[(x, y, dir)]
    dir = turn_around(dir)
    distance_to_e[(x, y, dir)] = v
   
# visit all states and see if they're on an optimal route
# making sure to ignore directionality
good_seats = set()   
for k in distance_from_s:
    if distance_from_s[k] + distance_to_e[k] == part1:
        x, y, _ = k
        good_seats.add((x, y))

print("Part 2:", len(good_seats))
