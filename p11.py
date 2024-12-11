FNAME = "in11.txt"

seq = [int(i) for i in open(FNAME).read().split()]
baseseq = seq[:]

# brute force for part 1
def blink(seq):
    result = []
    for i in seq:
        if i == 0:
            result.append(1)
        elif len(str(i)) % 2 == 0:
            ii = str(i)
            j = len(ii)
            result.append(int(ii[:j//2]))
            result.append(int(ii[j//2:]))
        else:
            result.append(i * 2024)
    return result
    
for _ in range(25):
    seq = blink(seq)
print("Part 1:", len(seq))

# need to be more clever for part 2--recursion with memoization to prune off a lot of the tree
# find size that a particular value, i, expands to after r blinks
memo = {}
def size(i, r):
    
    ii = str(i)
    j = len(ii)
    
    if (i, r) in memo:
        return memo[(i, r)]
    elif r == 0:
        return 1
    elif i == 0:
        x = size(1, r - 1)
    elif j % 2 == 0:
        x = size(int(ii[:j//2]), r - 1) + size(int(ii[j//2:]), r - 1)
    else:
        x = size(i * 2024, r - 1)
    memo[(i, r)] = x
    return x
    
seq = baseseq[:]
print("Part 1:", sum(size(i, 25) for i in seq))
seq = baseseq[:]
print("Part 2:", sum(size(i, 75) for i in seq))
