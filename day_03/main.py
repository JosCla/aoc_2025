#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def partOne(lines):
    total = 0
    for l in lines:
        # find digit 1
        d1_val = 0
        d1_pos = 0
        for i in range(0, len(l) - 1):
            if int(l[i]) > d1_val:
                d1_val = int(l[i])
                d1_pos = i

        # find digit 2
        d2_val = 0
        for i in range(d1_pos + 1, len(l)):
            if int(l[i]) > d2_val:
                d2_val = int(l[i])

        total += (d1_val * 10) + d2_val

    return total

def partTwo(lines):
    total = 0
    for l in lines:
        d_agg = ''
        prev_d_pos = -1
        for d in range(0, 12):
            d_val = 0
            d_pos = 0
            for i in range(prev_d_pos + 1, len(l) - (11 - d)):
                if int(l[i]) > d_val:
                    d_val = int(l[i])
                    d_pos = i
            prev_d_pos = d_pos
            d_agg += str(d_val)
        # print(l + ': ' + d_agg)
        total += int(d_agg)
    return total

print("Part One:", partOne(lines))
print("Part Two:", partTwo(lines))
