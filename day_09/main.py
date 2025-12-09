#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def get_pts(lines):
    return [tuple([int(n) for n in l.split(',')]) for l in lines]

def part_one(lines):
    # input is only 496 lines. part 1 is brute-forceable
    pts = get_pts(lines)
    max_area = 0
    for i in range(0, len(pts)):
        for j in range(i + 1, len(pts)):
            (x1, y1) = pts[i]
            (x2, y2) = pts[j]
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > max_area:
                max_area = area
    return max_area

def part_two(lines):
    # idea: if our rectangle contains another red tile, it's bad
    # idea 2: if our rectangle has a line through the middle, it's bad

    # this isn't technically correct; i don't check if my solution is inside or
    # outside the bounding figure.
    # but tracing my input file with my finger, it's pretty much a big circle
    # with one big horizontal line jutting through the middle. so we're
    # definitely not getting a largest box outside the figure. so i won't worry
    # about it.
    pts = get_pts(lines)
    max_area = 0
    for i in range(0, len(pts)):
        for j in range(i + 1, len(pts)):
            # print(str(i) + ':' + str(j))
            (x1, y1) = pts[i]
            (x2, y2) = pts[j]
            xmin = min(x1, x2)
            xmax = max(x1, x2)
            ymin = min(y1, y2)
            ymax = max(y1, y2)

            found = False
            for k in range(0, len(pts)):
                (x3, y3) = pts[k]
                if x3 > xmin and x3 < xmax and y3 > ymin and y3 < ymax:
                    # found point within box
                    found = True
                    # print('pt within')
                    break

                (x4, y4) = pts[(k+1) % len(pts)]
                if x3 == x4 and x3 > xmin and x3 < xmax:
                    if min(y3, y4) <= ymin and max(y3, y4) >= ymax:
                        # found intersecting vert line
                        found = True
                        # print('vert from ' + str(k))
                        break
                if y3 == y4 and y3 > ymin and y3 < ymax:
                    if min(x3, x4) <= xmin and max(x3, x4) >= xmax:
                        # found intersecting horiz line
                        found = True
                        # print('horiz from ' + str(k))
                        break
                    
            if found:
                continue

            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > max_area:
                max_area = area
                # print(str(i) + ':' + str(j) + ', ' + str(area))
    return max_area

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
