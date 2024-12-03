import re

FNAME = "in3.txt"

stream = open(FNAME).read()

# extract all the legitimate mul commands
commands = re.findall("mul\(\-?\d+,-?\d+\)", stream) # e.g. mul(23, 40)
    
# loop through them evaluating and summing
total = 0
for i in commands:
    a, b = re.findall('-?\d+', i)
    total += int(a) * int(b)

print("Part 1:", total)

# now include the do and don't commands
commands = re.findall("(mul\(\-?\d+,-?\d+\)|do\(\)|don't\(\))", stream)

# same idea as before, except "don't" disables counting until "do()"
total = 0
count = True # initially enabled
for command in commands:
    if command == "do()":
        count = True
    elif command == "don't()":
        count = False
    elif count: # must be a mul
        a, b = re.findall('-?\d+', command)
        total += int(a) * int(b)

print("Part 2:", total)
