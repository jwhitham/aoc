
import collections

problem = open("input", "rt")
out = open("reference", "wt")

data1 = []
data2 = []
for line in problem:
    data1.append([])
    data2.append([])
    for col in line.strip():
        data1[-1].append(col)
        data2[-1].append(col)

def trip(sy, sx, dy, dx):
    y = sy
    x = sx
    y += dy
    x += dx
    while (0 <= y < len(data1)) and (0 <= x < len(data1[0])):
        if data1[y][x] == "#":
            return 1
        elif data1[y][x] == "L":
            return 0
        else:
            y += dy
            x += dx

    return 0

def display():
    occ = 0
    for y in range(len(data1)):
        out.write("".join(data1[y]))
        out.write("\n")
        for v in data1[y]:
            if v == "#":
                occ += 1
    out.write(str(occ))
    out.write("\n")

display()
change = True
while change:
    change = False
    for y in range(len(data1)):
        for x in range(len(data1[0])):
            if data1[y][x] in "L#":
                count = (trip(y, x, -1, -1) + 
                         trip(y, x, -1, 0) + 
                         trip(y, x, -1, 1) + 
                         trip(y, x, 0, 1) + 
                         trip(y, x, 0, -1) + 
                         trip(y, x, 1, -1) + 
                         trip(y, x, 1, 0) + 
                         trip(y, x, 1, 1))
                if data1[y][x] == "#":
                    # occupied
                    if count >= 5:
                        # became unoccupied
                        change = True
                        data2[y][x] = "L"
                    else:
                        data2[y][x] = "#"
                else:
                    # unoccupied
                    if count == 0:
                        # became occupied
                        change = True
                        data2[y][x] = "#"
                    else:
                        data2[y][x] = "L"

    (data1, data2) = (data2, data1)
    display()
