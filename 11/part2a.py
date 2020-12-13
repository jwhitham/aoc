
import collections

problem = open("input", "rt")
out = open("x", "wt")
aux = open("x2", "wt")

data1 = []
data2 = []
for line in problem:
    data1.append([])
    data2.append([])
    for col in line.strip():
        data1[-1].append(col)
        data2[-1].append(0)

height = len(data1)
width = len(data1[0])
VACANT = 0x10
OCCUPIED = 0x20
COUNTER = 0xf

def trip(sy, sx, dy, dx):
    y = sy
    x = sx
    y += dy
    x += dx
    while (0 <= y < height) and (0 <= x < width):
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
        for v in data2[y]:
            aux.write(str(v & COUNTER))
        aux.write("\n")
        for v in data1[y]:
            if v == "#":
                occ += 1
    out.write(str(occ))
    out.write("\n")
    aux.write(str(occ))
    aux.write("\n")

display()

change = True
while change:
    change = False

    # Initial flags for these passes
    north_flag = []
    south_flag = []
    northwest_flag = []
    southwest_flag = []
    northeast_flag = []
    southeast_flag = []
    for x in range(width):
        north_flag.append(0)
        south_flag.append(0)
        northwest_flag.append(0)
        southwest_flag.append(0)
        northeast_flag.append(0)
        southeast_flag.append(0)

    # Pass from the northwest
    for y in range(height):
        west_flag = 0
        for x in range(width):
            if data1[y][x] == ".":
                data2[y][x] = 0
                if x > 0:
                    northeast_flag[x - 1] = northeast_flag[x]
            else:
                if data1[y][x] == "L":
                    data2[y][x] = VACANT
                else:
                    data2[y][x] = OCCUPIED
                    
                data2[y][x] += (west_flag + north_flag[x] +
                                northeast_flag[x] + northwest_flag[x])

                if data1[y][x] == "L":
                    west_flag = 0       # unoccupied
                    north_flag[x] = 0
                    if x > 0:
                        northeast_flag[x - 1] = 0
                else:
                    west_flag = 1       # occupied
                    north_flag[x] = 1
                    if x > 0:
                        northeast_flag[x - 1] = 1

        northeast_flag[width - 1] = 0

        # northwest flag requires reverse iteration
        northwest_flag[0] = 0
        for x in reversed(range(1, width)):
            if data2[y][x - 1] & OCCUPIED:
                northwest_flag[x] = 1
            elif data2[y][x - 1] & VACANT:
                northwest_flag[x] = 0
            else:
                northwest_flag[x] = northwest_flag[x - 1]

    # Pass from the southeast
    for y in reversed(range(height)):
        east_flag = 0
        for x in reversed(range(width)):
            if data2[y][x] == 0:
                data1[y][x] = "."
                if x < (width - 1):
                    southwest_flag[x + 1] = southwest_flag[x]
            else:
                data2[y][x] += (east_flag + south_flag[x] +
                                southeast_flag[x] + southwest_flag[x])

                if data2[y][x] & VACANT:
                    east_flag = 0       # unoccupied
                else:
                    east_flag = 1       # occupied
           
                count = data2[y][x] & COUNTER
                if not (data2[y][x] & VACANT):
                    # occupied
                    if count >= 5:
                        # became unoccupied
                        change = True
                        data1[y][x] = "L"
                    else:
                        data1[y][x] = "#"

                    south_flag[x] = 1
                    if x < (width - 1):
                        southwest_flag[x + 1] = 1
                else:
                    # unoccupied
                    if count == 0:
                        # became occupied
                        change = True
                        data1[y][x] = "#"
                    else:
                        data1[y][x] = "L"

                    south_flag[x] = 0
                    if x < (width - 1):
                        southwest_flag[x + 1] = 0

        # propagate southern flags
        southwest_flag[0] = 0
        southeast_flag[width - 1] = 0
        for x in (range(width - 1)):
            if data2[y][x + 1] & OCCUPIED:
                southeast_flag[x] = 1
            elif data2[y][x + 1] & VACANT:
                southeast_flag[x] = 0
            else:
                southeast_flag[x] = southeast_flag[x + 1]

    display()
