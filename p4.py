from aoc_utils import DIRECTIONS8

FNAME = "in4.txt"

grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

# child word search algo
# first look for X's, then look all possible directions from there for the rest
count = 0
for x in range(0, width):
    for y in range(0, height):
        if grid[y][x] == 'X':
            for dx, dy in DIRECTIONS8:
                # make sure we won't go past the edge of the board in the next three letters
                if 0 <= x + 3 * dx < width and 0 <= y + 3 * dy < height:
                    a = grid[y + 1 * dy][x + 1 * dx]
                    b = grid[y + 2 * dy][x + 2 * dx]
                    c = grid[y + 3 * dy][x + 3 * dx]
                    if a + b + c == "MAS":
                        count += 1
print("Part1:", count)

# find an A, extract its two diagonals, then check if they're valid
count = 0
for x in range(1, width - 1):
    for y in range(1, height - 1):
        if grid[y][x] == 'A':
            a = grid[y + 1][x + 1] + grid[y - 1][x - 1]
            b = grid[y - 1][x + 1] + grid[y + 1][x - 1]
            if a in ['MS', 'SM'] and b in ['MS', 'SM']:
                count += 1
print("Part2:", count)
