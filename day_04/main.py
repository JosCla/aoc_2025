#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def get_num_surr(lines, row, col):
    total = 0
    row_min = max(row - 1, 0)
    row_max = min(row + 1, len(lines) - 1)
    col_min = max(col - 1, 0)
    col_max = min(col + 1, len(lines[0]) - 1)
    for i in range(row_min, row_max + 1):
        for j in range(col_min, col_max + 1):
            if i == row and j == col:
                continue
            if lines[i][j] == '@':
                total += 1
    return total

def remove_rolls(lines):
    total = 0
    to_remove = []
    for row in range(0, len(lines)):
        for col in range(0, len(lines[0])):
            if lines[row][col] != '@':
                continue
            surr = get_num_surr(lines, row, col)
            if surr < 4:
                total += 1
                to_remove.append((row, col))

    for (r_row, r_col) in to_remove:
        lines[r_row][r_col] = '.'

    return (lines, total)

def partOne(lines):
    lines = [list(l) for l in lines]
    (lines, total) = remove_rolls(lines)
    return total

def partTwo(lines):
    total = 0
    lines = [list(l) for l in lines]
    while True:
        (lines, curr_t) = remove_rolls(lines)
        total += curr_t
        if curr_t == 0:
            break
    return total

print("Part One:", partOne(lines))
print("Part Two:", partTwo(lines))
