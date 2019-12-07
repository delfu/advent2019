from IntCodes import IntCodes
from test import expect

runner = IntCodes()

"""
print(runner.run_program([1002, 4, 3, 4, 33]))
print(runner.run_program([3, 0, 4, 0, 99], 50))
print(runner.run_program([1101, 100, -1, 4, 0]))

"""
with open("5.in") as program_file:
    program = program_file.readline().strip()
    program = program.split(",")
    program = list(map(lambda x: int(x), program))

    runner.run_program(program, [5])
