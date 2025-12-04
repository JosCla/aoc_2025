#!/bin/python3

import sys
lines = []
for line in sys.stdin:
    lines.append(line[:-1])

def partOne(lines):
    total = 0
    ranges = lines[0].split(',')
    for r in ranges:
        # print(r)
        [r1, r2] = r.split('-')
        min_len = len(r1)
        max_len = len(r2)
        r1 = int(r1)
        r2 = int(r2)

        for i in range(min_len, max_len + 1):
            if i % 2 == 1:
                continue
            rep_len = int(i / 2)
            min_at_len = int('1' + ('0' * (rep_len - 1)))
            for i in range(min_at_len, min_at_len * 10):
                curr = int(str(i) + str(i))
                if curr >= r1 and curr <= r2:
                    # print(curr)
                    total += curr

        # print('')
    return total

def partTwo(lines):
    total = 0
    ranges = lines[0].split(',')
    for r in ranges:
        # print(r)
        [r1, r2] = r.split('-')
        min_len = len(r1)
        max_len = len(r2)
        r1 = int(r1)
        r2 = int(r2)

        found = set()
        for total_len in range(min_len, max_len + 1):
            for rep_len in range(1, total_len):
                if total_len % rep_len != 0:
                    continue
                num_reps = int(total_len / rep_len)
                # print(str(rep_len) + ', ' + str(num_reps))
                min_at_len = int('1' + ('0' * (rep_len - 1)))
                for j in range(min_at_len, min_at_len * 10):
                    curr = int(str(j) * num_reps)
                    if curr >= r1 and curr <= r2 and curr not in found:
                        # print(curr)
                        total += curr
                        found.add(curr)

        # print('')
    return total
    return 1

print("Part One:", partOne(lines))
print("Part Two:", partTwo(lines))
