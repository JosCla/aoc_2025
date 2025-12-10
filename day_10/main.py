#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

class Machine:
    def __init__(self, line):
        parts = line.split(' ')
        self.lights = parts[0][1:-1]
        self.jolts = list(map(int, parts[-1][1:-1].split(',')))
        self.btns = [list(map(int, n[1:-1].split(','))) for n in parts[1:-1]]

def get_machines(lines):
    return [Machine(l) for l in lines]

def get_valid_presses(lights, btns):
    curr_lights = '.' * len(lights)
    return get_valid_presses_rec(lights, curr_lights, btns)

def get_valid_presses_rec(target_lights, curr_lights, rem_btns):
    # base case: no buttons left
    if len(rem_btns) == 0:
        if target_lights == curr_lights:
            return [[]]
        else:
            return []

    # recursive case: split to either press or not press next button
    no_press = get_valid_presses_rec(target_lights, curr_lights, rem_btns[1:])
    acc = [[0] + a for a in no_press]

    curr_btn = rem_btns[0]
    press_lights = list(curr_lights)
    for b in curr_btn:
        if press_lights[b] == '.':
            press_lights[b] = '#'
        else:
            press_lights[b] = '.'
    next_lights = ''.join(press_lights)
    press = get_valid_presses_rec(target_lights, next_lights, rem_btns[1:])
    acc += [[1] + a for a in press]

    return acc

def part_one(lines):
    machs = get_machines(lines)
    total = 0
    for m in machs:
        valids = get_valid_presses(m.lights, m.btns)
        mach_min = 10000
        for presses in valids:
            num_press = sum(presses)
            if num_press < mach_min:
                mach_min = num_press
        total += mach_min
    return total

def part_two(lines):
    return 1

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
