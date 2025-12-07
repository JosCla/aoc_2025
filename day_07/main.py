#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def sim(lines):
    # search first line for S, start with single beam below
    beams = {lines[0].index('S'): 1}
    total_splits = 0

    # then iterate through remaining lines, splitting beams as applicable
    for l in lines[2:]:
        new_beams = {}
        for (b_loc, b_str) in beams.items():
            if l[b_loc] == '^':
                # split strength into adjacent columns
                loc_1 = b_loc - 1
                loc_2 = b_loc + 1
                if loc_1 in new_beams:
                    new_beams[loc_1] += b_str
                else:
                    new_beams[loc_1] = b_str
                if loc_2 in new_beams:
                    new_beams[loc_2] += b_str
                else:
                    new_beams[loc_2] = b_str

                total_splits += 1
            else:
                # just continue in same column
                if b_loc in new_beams:
                    new_beams[b_loc] += b_str
                else:
                    new_beams[b_loc] = b_str
        beams = new_beams

    total_str = 0
    for s in beams.values():
        total_str += s

    return (total_splits, total_str)

def part_one(lines):
    (total_splits, total_str) = sim(lines)
    return total_splits

def part_two(lines):
    (total_splits, total_str) = sim(lines)
    return total_str

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
