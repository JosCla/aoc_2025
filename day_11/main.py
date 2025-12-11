#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def get_network(lines):
    net = {}
    for l in lines:
        spl = l.split(': ')
        key = spl[0]
        vals = spl[1].split(' ')
        net[key] = vals
    return net

def get_paths_to_out(net, curr, memo):
    if curr == 'out':
        # base case: we're at out
        return 1
    if curr in memo:
        # base case: already in memo
        return memo[curr]

    # recursive case: traverse all valid paths in net
    paths = net[curr]
    total = 0
    for p in paths:
        curr_out = get_paths_to_out(net, p, memo)
        total += curr_out
    memo[curr] = total
    return total

# idea: now we kinda have 4 return values. how many paths add dac, fft,
# neither, or both?
# and then if our current node is dac or fft, that adds dac or fft
def get_paths_to_out_2(net, curr, memo):
    if curr == 'out':
        # base case: we're at out
        return (1, 0, 0, 0)
    if curr in memo:
        # base case: already in memo
        return memo[curr]

    # recursive case: traverse all valid paths in net
    paths = net[curr]
    total_nn = 0
    total_nd = 0
    total_fn = 0
    total_fd = 0
    for p in paths:
        (nn, nd, fn, fd) = get_paths_to_out_2(net, p, memo)
        if curr == 'dac':
            total_nd += (nn + nd)
            total_fd += (fn + fd)
        elif curr == 'fft':
            total_fn += (nn + fn)
            total_fd += (nd + fd)
        else:
            total_nn += nn
            total_nd += nd
            total_fn += fn
            total_fd += fd
    total = (total_nn, total_nd, total_fn, total_fd)
    memo[curr] = total
    return total

def part_one(lines):
    net = get_network(lines)
    if 'you' not in net:
        return -1
    return get_paths_to_out(net, 'you', {})

def part_two(lines):
    net = get_network(lines)
    if 'svr' not in net:
        return -1
    (_, _, _, total_fd) = get_paths_to_out_2(net, 'svr', {})
    return total_fd

print("Part One:", part_one(lines))
print("Part Two:", part_two(lines))
