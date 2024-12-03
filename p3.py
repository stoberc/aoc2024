import pdb
import re

FNAME = "in3.txt"

stream = open(FNAME).read()

commands = re.findall("mul\(\-?\d+,-?\d+\)", stream)
    
total = 0
for i in commands:
    a, b = re.findall('-?\d+', i)
    total += int(a) * int(b)

print("Part 1:", total)

commands = re.findall("(mul\(\-?\d+,-?\d+\))|(do\(\))|(don't\(\))", stream)

filtered_commands = []
for a, b, c in commands:
    if a:
        filtered_commands.append(a)
    elif b:
        filtered_commands.append(b)
    elif c:
        filtered_commands.append(c)

total = 0
count = True
for command in filtered_commands:
    if command == 'do()':
        count = True
    elif command == "don't()":
        count = False
    elif count:
        a, b = re.findall('-?\d+', command)
        total += int(a) * int(b)

print("Part 2:", total)

pdb.set_trace()
