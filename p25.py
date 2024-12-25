FNAME = "in25.txt"

chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
    
keys = []
locks = []

# could probably do this more easily if I remembered how to do a quick transpose
# then just count '#' in each column (now row)
for chunk in chunks:
    grid = [list(line) for line in chunk]
    height = len(grid)
    width = len(grid[0])
    if '.' in grid[0]:
        key = []
        for x in range(width):
            key_height = 0
            while grid[height - 1 - key_height - 1][x] == '#':
                key_height += 1
            key.append(key_height)
        keys.append(key)
    else:
        lock = []
        for x in range(width):
            lock_height = 0
            while grid[1 + lock_height][x] == '#':
                lock_height += 1
            lock.append(lock_height)
        locks.append(lock)

part1 = 0
for k in keys:
    for l in locks:
        if all(kh + lh <= 5 for kh, lh in zip(k, l)):
            part1 += 1            
print("Part 1:", part1)
