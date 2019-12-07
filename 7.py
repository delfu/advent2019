from IntCodes import IntCodes
from copy import deepcopy
from itertools import permutations


with open("7.in") as input:
    initial_program = list(map(lambda x: int(x), input.readline().strip().split(",")))

max_val = 0
best_combo = None
combos = list(permutations([5, 6, 7, 8, 9]))
for combo in combos:
    inputs = [[c] for c in combo]
    inputs[0].insert(1, 0)
    amps = [
        IntCodes().run_program(deepcopy(initial_program), input) for input in inputs
    ]

    outputs = []
    i = 0
    while True:
        try:
            output = next(amps[i])
            if output is None:
                break
            outputs.append(output)
            i = (i + 1) % 5
            inputs[i].append(output)
        except StopIteration:
            break
    if outputs[-1] > max_val:
        max_val = outputs[-1]
        best_combo = combo

print(best_combo, max_val)
