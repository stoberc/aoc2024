from aoc_utils import *
import re

FNAME = "in14.txt"
HEIGHT = 103
WIDTH = 101

def parse_line(line):
    return [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers

robots = [parse_line(line) for line in open(FNAME).read().splitlines()]

# calculate the location of a robot t time steps from now
def simulate(robot, t):
    px, py, vx, vy = robot
    return (px + vx * t) % WIDTH, (py + vy * t) % HEIGHT

# score a layout of robots using the quadrant scoring scheme specified in the problem
def score(robots):
    a, b, c, d = 0, 0, 0, 0
    for x, y in robots:
        if x < WIDTH // 2:
            if y < HEIGHT // 2:
                a += 1
            elif y > HEIGHT // 2:
                b += 1
        elif x > WIDTH // 2:
            if y < HEIGHT // 2:
                c += 1
            elif y > HEIGHT // 2:
                d += 1
    return a * b * c * d
    
part1 = score(simulate(robot, 100) for robot in robots)
print("Part 1:", part1)

# need to retain all robot state if we're going to iterate repeatedly
# so this one also returns velocity
def simulate(robot, t):
    px, py, vx, vy = robot
    return (px + vx * t) % WIDTH, (py + vy * t) % HEIGHT, vx, vy
        
# need to ID candidate generations, then render them to take a closer look
# low standard deviation seems like a good candidate,
# but didn't feel like messing with the complexity

# failed attempt - if ALL robots are arranged in a tree, 
# perhaps the xrange will be reduced
# wrong since *most* robots are part of the tree
def xdispersion(robots):
    xmin = min(x for x, _, _, _ in robots)
    xmax = max(x for x, _, _, _ in robots)
    return xmax - xmin < 97
    
# successful attempt -
# perhaps cumulative manhattan distance from center will be reduced when
# robots are tightly packed
# assumed tree would be centered; luckily it was close enough
def candidate(robots):
    return sum(abs(x - 51) + abs(y - 53) for x, y, _, _ in robots) < 18000 # experimentally tuned

part2 = 0
while True:
    robots = [simulate(robot, 1) for robot in robots]
    part2 += 1
    #if part2 % 1000 == 0:
    #    print("Generation:", part2)
    if candidate(robots):
        render([(x, y) for x, y, _, _ in robots])
        print("Part 2:", part2)
        break
    