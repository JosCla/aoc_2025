#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def get_shapes_and_regions(lines):
    # first shapes
    shapes = []
    i = 0
    while True:
        if 'x' in lines[i]:
            break
        shapes.append(lines[i+1:i+4])
        i += 5

    # then regions
    regions = []
    for j in range(i, len(lines)):
        l_spl = lines[j].split(': ')
        spl_left = list(map(int, l_spl[0].split('x')))
        spl_right = list(map(int, l_spl[1].split(' ')))
        regions.append((spl_left[0], spl_left[1], spl_right))

    return (shapes, regions)

# bruhhh final day part 1 is usually super easy!!!
# this one is mad hard!!!!!
# initial smattering of thoughts:
#
# certain pieces naturally fit together very well, like in the sample input:
#   3 + 5 + 3 = 3x8 solid block
#   0 + 1 + 3 = 3x8 solid block
#   0 + 2 + 0 = 3x8 solid block
#   4 is the only piece that very naturally fits with itself
# my actual input has a pretty similar situation, with, e.g., 3 + 0 + 2 = 3x7
# but this doesn't work universally... even in the sample input, there are some
# very twiddly combos!
# 
# could there be some DP here? like find out how to pack fewer presents in a
# smaller region, and leverage that for a larger one?
#
# can we identify any regions as trivially good/bad?
# trivial bad = total units of all presents > total space
#   actually this is like half the input
# trivial good = you could replace all gifts with 3x3 and be okay
#
# are you kidding me
def part_one(lines):
    (shapes, regions) = get_shapes_and_regions(lines)

    # identify how many units each present type has
    s_units = []
    for s in shapes:
        units = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if s[i][j] == '#':
                    units += 1
        s_units.append(units)

    # identify how many free units each region has
    total = 0
    for (l, w, presents) in regions:
        # check for trivially bad regions
        total_units = l * w
        needed_units = sum([n * u for (n, u) in zip(presents, s_units)])
        free_units = total_units - needed_units
        if free_units < 0:
            continue

        # check for trivially good regions
        l_simple = int(l / 3)
        w_simple = int(w / 3)
        free_units_simple = l_simple * w_simple
        needed_units_simple = sum(presents)
        if free_units_simple >= needed_units_simple:
            total += 1
            continue

        # apparently nothing ever makes it this far?????
        raise Exception("Not a very merry Christmas!!!")
        
    return total

def part_two(lines):
    return "Merry Christmas!"

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
