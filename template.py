import pdb
from collections import defaultdict, deque # usage: x = defaultdict(lambda: float('inf')) or defaultdict(list)
from aoc_utils import *
import re
from math import prod

FNAME = "in24.txt"
    
def parse_line(line):
    return int(line)
    #return [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers

#chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
#data = [[parse_line(line) for line in chunk] for chunk in chunks]

data = [parse_line(line) for line in open(FNAME).read().splitlines()] # in chunks[0]]

#data = [int(i) for i in open(FNAME).read().split(',')]

#grid = [list(line) for line in open(FNAME).read().splitlines()]
#height = len(grid)
#width = len(grid[0])

part1 = 0
print("Part 1:", part1)

part2 = 0
print("Part 2:", part2)

pdb.set_trace()
