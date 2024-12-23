from collections import defaultdict

FNAME = "in23.txt"
    
# load graph from file
graph = defaultdict(set)
for line in open(FNAME).read().splitlines():
    a,b = line.split('-')
    graph[a].add(b)
    graph[b].add(a)

# find the set of all sorted trios
trios = set()
for a in graph:
    for b in graph[a]:
        for c in graph[a]:
            if b in graph[c] and c in graph[b]:
                trio = [a, b, c]
                trio.sort()
                trios.add(tuple(trio))

# count the number of trios with a node that starts with 't'
part1 = 0                
for a, b, c in trios:
    if a[0] == 't' or b[0] == 't' or c[0] == 't':
        part1 += 1
print("Part 1:", part1)

# find all subsets of a set
# need to index, so input must be list
def powerset(set_list):
    if len(set_list) == 0:
        return [[]]
    subpowerset = powerset(set_list[1:])
    return [[set_list[0]] + s for s in subpowerset] + subpowerset
    
# time to solve an NP-complete problem...
# this only works because the max degree of any node is 13, 
# and looping through 2 ** 13 possible subsets for each node is tractable
# incidentally *every* node has a degree of 13
max_clique = []
for a in graph:
    for neighbor_subset in powerset(list(graph[a])):
        is_clique = True
        for n in neighbor_subset:
            if any(n2 not in graph[n] for n2 in neighbor_subset if n2 != n):
                is_clique = False
                break
        if is_clique and len(neighbor_subset + [a]) > len(max_clique):
            max_clique = neighbor_subset + [a]
        
max_clique.sort()
print("Part 2:", ','.join(max_clique))
