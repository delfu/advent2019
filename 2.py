op_codes = [1, 2, 99]
from IntCodes import IntCodes

"""
runner = IntCodes()
print(runner.run_program([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]))
print(runner.run_program([1, 0, 0, 0, 99]))
print(runner.run_program([2, 3, 0, 3, 99]))
print(runner.run_program([2, 4, 4, 5, 99, 0]))
print(runner.run_program([1, 1, 1, 4, 99, 5, 6, 0, 99]))
"""

"""
# runner for part 1
with open("2.in") as input:
    for line in input:
        line = line.strip().split(",")
        program = [int(p) for p in line]
        print(runner.run_program(program))
"""


if __name__ == "__main__":
    from copy import deepcopy

    def main():
        with open("2.in") as input:
            for line in input:
                line = line.strip().split(",")
                initial_program = [int(p) for p in line]

            runner = IntCodes()

            for i in range(100):
                for j in range(100):
                    program = deepcopy(initial_program)
                    program[1] = i
                    program[2] = j
                    exit_code, memory = runner.run_program(program)
                    if memory[0] == 19690720:
                        print("found solution, noun, verb:", i, j, 100 * i + j)
                        return

    main()
