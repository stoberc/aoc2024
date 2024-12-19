FNAME = "in19.txt"

chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
base_towels = chunks[0][0].split(', ')
target_towels = chunks[1]

# check if there's any way to build some towel
def is_possible(target_towel):
    if target_towel == "":
        return True
    for base_towel in base_towels:
        l = len(base_towel)
        if l <= len(target_towel) and target_towel[:l] == base_towel and is_possible(target_towel[l:]):
            return True
    return False
    
part1 = sum(is_possible(t) for t in target_towels)
print("Part 1:", part1)

# check HOW MANY ways there are to build some towel
memo = {} # lots of repeated subchunks and very large final answer--memoization needed
def num_possibilities(target_towel):
    if target_towel in memo:
        return memo[target_towel]
    if target_towel == "":
        return 1
    count = 0
    for base_towel in base_towels:
        l = len(base_towel)
        if l <= len(target_towel) and target_towel[:l] == base_towel and is_possible(target_towel[l:]):
            count += num_possibilities(target_towel[l:])
    memo[target_towel] = count
    return count
    
part2 = sum(num_possibilities(t) for t in target_towels)
print("Part 2:", part2)
