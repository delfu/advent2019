from IntCodes import IntCodes
from test import expect

runner = IntCodes()

print(runner.run_program([99]))
print(runner.run_program([1, 5, 6, 0, 99, 5, 16]))
