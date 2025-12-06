#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def split_lines(lines):
    # first find common spaces between all lines
    space_sets = [set([i for (i, n) in enumerate(l) if n == ' ']) for l in lines]
    space_inds = space_sets[0]
    for s in space_sets:
        space_inds = space_inds.intersection(s)
    space_inds = list(space_inds)
    space_inds.sort()
    space_inds = [-1] + space_inds

    # then split all the lines accordingly
    lines_fnl = []
    for l in lines:
        curr_fnl = []
        for i in range(0, len(space_inds) - 1):
            start = space_inds[i] + 1
            end = space_inds[i + 1]
            curr_fnl.append(l[start:end])
        curr_fnl.append(l[space_inds[len(space_inds) - 1] + 1:])
        lines_fnl.append(curr_fnl)

    return lines_fnl

def part_one(lines):
    # print(split_lines(lines))
    # for l in lines:
    #     print(l[:50])

    lines_spl = split_lines(lines)
    total = 0
    for col in range(0, len(lines_spl[0])):
        op = lines_spl[len(lines_spl) - 1][col].strip()
        inputs = [l[col].strip() for l in lines_spl[:-1]]
        eq = op.join(inputs)
        res = eval(eq)
        total += res
    return total

def part_two(lines):
    lines_spl = split_lines(lines)
    total = 0
    for col in range(0, len(lines_spl[0])):
        op = lines_spl[len(lines_spl) - 1][col].strip()

        inputs_raw = [l[col] for l in lines_spl[:-1]]
        inputs = []
        for i_col in range(0, len(inputs_raw[0])):
            inputs.append((''.join([r[i_col] for r in inputs_raw])).strip())

        eq = op.join(inputs)
        res = eval(eq)
        total += res
    return total

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
