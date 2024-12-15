from aoc_utils import UP, DOWN, LEFT, RIGHT

FNAME = "in15.txt"

DLUT = {'^':UP, 'v': DOWN, '<':LEFT, '>':RIGHT}

chunks =  open(FNAME).read().split('\n\n')
grid = [list(line) for line in chunks[0].split()]
height = len(grid)
width = len(grid[0])
commands = chunks[1].replace('\n','')

# find robot starting location and clear it
for x in range(width):
    for y in range(height):
        if grid[y][x] == "@":
            rx, ry = x, y
            grid[y][x] = '.'
            
# loop through each command, executing it if possible
for command in commands:
    dx, dy = DLUT[command]
    nx, ny = rx + dx, ry + dy # adjacent cell
    destx, desty = nx, ny # will be cell at end of push chain 
    while grid[desty][destx] == 'O':
        destx += dx
        desty += dy
    # if the push chain ends in a wall, do nothing
    if grid[desty][destx] == '#':
        continue
    assert grid[desty][destx] == '.' # the push chain must end in empty space
    
    # if there's a box in the way, we can basically swap it into the last empty spot
    if grid[ny][nx] == 'O':    
        grid[ny][nx] = '.'
        grid[desty][destx] = 'O'
    rx, ry = nx, ny # robot advances
   
# apply part 1 scoring algo   
part1 = 0
for x in range(width):
    for y in range(height):
        if grid[y][x] == 'O':
            part1 += 100 * y + x
print("Part 1:", part1)

# reset the grid and build the doubled grid
grid = [list(line) for line in chunks[0].split()]
newgrid = []
for line in grid:
    row = []
    for i in line:
        if i == 'O':
            row.append('[')
            row.append(']')
        elif i == '@':
            row.append('@')
            row.append('.')
        else:
            row.append(i)
            row.append(i)
    newgrid.append(row)
grid = newgrid
height = len(grid)
width = len(grid[0])

# find robot starting location and clear it
for x in range(width):
    for y in range(height):
        if grid[y][x] == "@":
            rx, ry = x, y
            grid[y][x] = '.'

# check if it's possible to push the target cell in the desired direction
def canpush(x, y, direction):
    if grid[y][x] == '.': # an empty is inherently pushable
        return True
    elif grid[y][x] == '#': # a wall can never be pushed
        return False
    assert grid[y][x] in '[]' # a box can MAYBE be pushed if the thing beyond can be pushed
    dx, dy = direction
    if direction in [RIGHT, LEFT]:
        return canpush(x + 2 * dx, y, direction)
    elif grid[y][x] == '[':
        return canpush(x, y + dy, direction) and canpush(x + 1, y + dy, direction)
    else:
        return canpush(x, y + dy, direction) and canpush(x - 1, y + dy, direction)
            
# push the target cell in the desired direction
# precondition: canpush(x, y, direction)
def push(x, y, direction):
    if grid[y][x] == '.': # pushing an empty space does nothing
        return
    elif grid[y][x] == '#': # pushing w/o checking if possible
        raise ValueError("Trying to push a wall!")
    assert grid[y][x] in '[]'
    dx, dy = direction
    if direction in [RIGHT, LEFT]:
        push(x + dx, y, direction)
        grid[y][x + dx] = grid[y][x]
        grid[y][x] = '.'
    elif grid[y][x] == '[':
        assert grid[y][x + 1] == ']'
        push(x, y + dy, direction)
        push(x + 1, y + dy, direction)
        grid[y + dy][x] = '['
        grid[y + dy][x + 1] = ']'
        grid[y][x] = '.'
        grid[y][x + 1] = '.'
    else:
        assert grid[y][x] == ']'
        assert grid[y][x - 1] == '['
        push(x, y + dy, direction)
        push(x - 1, y + dy, direction)
        grid[y + dy][x] = ']'
        grid[y + dy][x - 1] = '['
        grid[y][x] = '.'
        grid[y][x - 1] = '.'

# attempt to apply all commands
for command in commands:
    dx, dy = DLUT[command]
    if canpush(rx + dx, ry + dy, (dx, dy)):
        push(rx + dx, ry + dy, (dx, dy))
        rx += dx
        ry += dy

# apply part 2 scoring algo  
part2 = 0
for x in range(width):
    for y in range(height):
        if grid[y][x] == '[':
            part2 += 100 * y + x
print("Part 2:", part2)
