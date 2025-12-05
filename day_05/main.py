#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def split_lines(lines):
    spl = lines.index('')
    ranges = [(int(l.split('-')[0]), int(l.split('-')[1])) for l in lines[:spl]]
    inds = [int(l) for l in lines[spl + 1:]]
    return (ranges, inds)

def part_one(lines):
    (ranges, inds) = split_lines(lines)
    total = 0
    for i in inds:
        for (r1, r2) in ranges:
            if i >= r1 and i <= r2:
                total += 1
                break
    return total

# does r1 overlap r2?
def range_overlaps(r1, r2):
    (r11, r12) = r1
    (r21, r22) = r2

    if r11 <= r21 and r12 >= r21:
        return True
    if r11 <= r22 and r12 >= r22:
        return True
    if r11 >= r21 and r12 <= r22:
        return True
    return False

# take existing set of range tuples, and combine in a new range
def merge_ranges(curr_ranges, new_range):
    # find all ranges that the new range overlaps with
    overlap = []
    no_overlap = []
    for c in curr_ranges:
        if range_overlaps(c, new_range):
            overlap.append(c)
        else:
            no_overlap.append(c)

    # merge all the overlapping ranges
    (min_range, max_range) = new_range
    for (o1, o2) in overlap:
        if o1 < min_range:
            min_range = o1
        if o2 > max_range:
            max_range = o2

    no_overlap.append((min_range, max_range))
    return no_overlap

def part_two(lines):
    (ranges, inds) = split_lines(lines)
    final_ranges = []
    for r in ranges:
        final_ranges = merge_ranges(final_ranges, r)
        # print(final_ranges)

    total = 0
    for (f1, f2) in final_ranges:
        total += (f2 - f1) + 1

    return total

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
