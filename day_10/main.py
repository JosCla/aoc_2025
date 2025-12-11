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

# idea 1: basically brute-force. start by pressing biggest button as much as
# possible, then move down to next button, etc
# issue: takes too long (and not necessarily correct)
def try_solve(btns, totals, depth):
    # base case: no more buttons! return 0 if solved successfully
    if len(btns) == 0:
        if max(totals) == 0:
            return 0
        else:
            return None

    # press next button a descending number of times until solveable
    btn = btns[0]
    max_presses = min([totals[b] for b in btn])
    for press in range(max_presses, -1, -1):
        if depth == 0:
            print(press)
        next_totals = [t for t in totals]
        for b in btn:
            next_totals[b] -= press
        best_presses = try_solve(btns[1:], next_totals, depth + 1)
        if best_presses is not None:
            return best_presses + press

# idea 2: press whichever button is "most aligned" with the target value
# issue: answer is not correct, generally
#   seems like it's actually surprisingly hard to just get a correct answer
#   so perhaps the solution space is quite constrained?
def try_solve_2(btns, totals):
    presses = 0
    totals_left = [t for t in totals]

    while True:
        dots = [sum([totals_left[n] for n in b]) for b in btns]
        if max(dots) == 0:
            return presses
        b = btns[dots.index(max(dots))]
        for n in b:
            totals_left[n] -= 1
            presses += 1

# idea 3: try to properly solve the system of equations
# say X is a column vector for how many times we press button x_i
# and say B is a vector whose columns are 0/1 for which slots are affected by
#   which button
# and say J is a column vector with the desired joltages
# then all valid solutions will have form BX = J, for J in the natural nums
#   (and we need to minimize sum(X))
#   (which is np-hard.)
#   (but if the solution-space is really constrained... might work out!)

# upon rref'ing: that's actually very helpful!
# pretty much all the inputs only have 1-2 meaningful degrees of freedom
#   (rarely 3, but never more!!!)
# they look like this, for instance:
# (Matrix([
# [1, 0, 0, 0, 0, 0,  3, 0,  50],
# [0, 1, 0, 0, 0, 0, -2, 0, -13],
# [0, 0, 1, 0, 0, 0,  1, 0,  12],
# [0, 0, 0, 1, 0, 0,  2, 0,  25],
# [0, 0, 0, 0, 1, 0, -1, 0,   0],
# [0, 0, 0, 0, 0, 1, -3, 0, -11],
# [0, 0, 0, 0, 0, 0,  0, 1,  20]]), (0, 1, 2, 3, 4, 5, 7))
# at that point, x_7 = 20, then vary x_6 and solve for 1-5
# helpfully, seems there's an extra tuple containing "fixed" params

# it works!!!
# it takes multiple minutes to run. but it works!!!

import sympy as sp
def try_solve_3_rec(to_vary, now_fixed, m_t_rref):
    # base case: nothing more to vary. try solution!
    if len(to_vary) == 0:
        soln = [f for f in now_fixed]
        for row in m_t_rref:
            curr_sol = -1 # which button we're solving
            for col in range(0, len(row)):
                if row[col] == 1:
                    curr_sol = col
                    break
            if curr_sol == -1:
                break

            other_press = sum([now_fixed[i] * row[i] for i in range(0, len(now_fixed))])
            curr_val = row[-1] - other_press
            soln[curr_sol] = curr_val

        if min(soln) < 0:
            return None
        for s in soln:
            if int(s) != s:
                return None
        return sum(soln)

    # recursive case: still more to vary
    (v, m) = to_vary[0]
    lowest = 10000
    for i in range(0, m + 1):
        next_fixed = [n for n in now_fixed]
        next_fixed[v] = i
        curr_presses = try_solve_3_rec(to_vary[1:], next_fixed, m_t_rref)
        if curr_presses is not None:
            if curr_presses < lowest:
                lowest = curr_presses
    return lowest

def try_solve_3(btns, totals):
    # construct and rref equation matrix
    m_cols = []
    for b in btns:
        col = [0] * len(totals)
        for n in b:
            col[n] = 1
        m_cols.append(col)
    m_cols.append(totals)

    m = sp.Matrix(m_cols)
    m_t = m.T
    (m_t_rref, fixed) = m_t.rref()
    # print((m_t_rref, fixed))

    # find which columns vary, and by how much
    to_vary = set([i for i in range(0, len(btns))]).difference(fixed)
    to_vary_limits = []
    for v in to_vary:
        btn = btns[v]
        max_presses = min([totals[b] for b in btn])
        to_vary_limits.append((v, max_presses))

    # brute-force try all combos
    now_fixed = [0] * len(btns)
    return try_solve_3_rec(to_vary_limits, now_fixed, m_t_rref.tolist())

def part_two(lines):
    machs = get_machines(lines)
    total = 0
    for (i, m) in enumerate(machs):
        print("Solving " + str(i))
        best_press = try_solve_3(m.btns, m.jolts)
        total += best_press
    return total

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
