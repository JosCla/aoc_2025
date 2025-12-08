#!/bin/python3

import sys
import math
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def get_point_list(lines):
    return [tuple(map(int, l.split(','))) for l in lines]

def get_dist(pt1, pt2):
    (x1, y1, z1) = pt1
    (x2, y2, z2) = pt2
    (dx, dy, dz) = (x2 - x1, y2 - y1, z2 - z1)
    return math.sqrt((dx * dx) + (dy * dy) + (dz * dz))

def get_sorted_dists(lines):
    dists = []
    pts = get_point_list(lines)
    for i in range(0, len(pts)):
        for j in range(i + 1, len(pts)):
            d = get_dist(pts[i], pts[j])
            dists.append((d, i, j))
    dists.sort()
    return dists

def part_one(lines):
    dists = get_sorted_dists(lines)
    circuits = [n for n in range(0, len(lines))]
    num_steps = 1000
    if len(lines) == 20:
        num_steps = 10

    # make shortest junctions
    for n in range(0, num_steps):
        (dist, i, j) = dists[n]
        circ_1 = circuits[i]
        circ_2 = circuits[j]
        circ_fnl = min(circ_1, circ_2)
        for k in range(0, len(circuits)):
            if circuits[k] == circ_1 or circuits[k] == circ_2:
                circuits[k] = circ_fnl

    # look for largest circuits
    circ_sizes = {}
    for c in circuits:
        if c not in circ_sizes:
            circ_sizes[c] = 1
        else:
            circ_sizes[c] += 1
    size_map = [(a, b) for (b, a) in circ_sizes.items()]
    size_map.sort(reverse = True)
    (s0, _) = size_map[0]
    (s1, _) = size_map[1]
    (s2, _) = size_map[2]

    return s0 * s1 * s2

def part_two(lines):
    pts = get_point_list(lines)
    dists = get_sorted_dists(lines)
    circuits = [n for n in range(0, len(lines))]

    # make shortest junctions until we just connected everything
    for n in range(0, len(dists)):
        (dist, i, j) = dists[n]
        circ_1 = circuits[i]
        circ_2 = circuits[j]
        circ_fnl = min(circ_1, circ_2)

        num_affected = 0
        for k in range(0, len(circuits)):
            if circuits[k] == circ_1 or circuits[k] == circ_2:
                circuits[k] = circ_fnl
                num_affected += 1

        if num_affected == len(circuits):
            (x1, _, _) = pts[i]
            (x2, _, _) = pts[j]
            return x1 * x2

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
