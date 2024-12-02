FNAME = "in1.txt"

listA = []
listB = []
for line in open(FNAME).read().splitlines():
    a, b = [int(i) for i in line.split()]
    listA.append(a)
    listB.append(b)
    
listA.sort()
listB.sort()
    
part1 = sum(abs(a - b) for a, b in zip(listA, listB))  
print("Part 1:", part1)

part2 = sum(i * listB.count(i) for i in listA)
print("Part 2:", part2)
