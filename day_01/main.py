#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def partOne(lines):
    pos = 50
    total_zeros = 0
    for l in lines:
        l_dir = l[0]
        l_amt = int(l[1:])
        if l_dir == 'L':
            l_amt = -l_amt

        pos += l_amt
        pos = pos % 100
        if pos < 0:
            pos += 100

        if pos == 0:
            total_zeros += 1

    return total_zeros

# 7599 too high
def partTwo(lines):
    pos = 50
    total_zeros = 0
    for l in lines:
        l_dir = l[0]
        l_amt = int(l[1:])
        if l_dir == 'L':
            l_amt = -l_amt

        prev_pos = pos
        pos += l_amt
        if pos >= 100:
            # twisted far enough right to go past 0
            total_zeros += int(pos / 100)
            pos = pos % 100
        elif pos < 0:
            # twisted far enough left to go past 0
            total_zeros += int(-pos / 100) + 1
            if prev_pos == 0:
                # if started at zero, don't double-count it
                total_zeros -= 1
            pos = pos % 100
        elif pos == 0:
            # twisted to exactly 0
            total_zeros += 1

        # print(l + ': ' + str(pos) + ', ' + str(total_zeros))

    return total_zeros

print("Part One:", partOne(lines))
print("Part Two:", partTwo(lines))
