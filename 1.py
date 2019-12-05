import math

cache = {}
def calculateFuel(mass):
  if mass < 9:
    return 0
  if mass in cache: 
    return cache[mass]
  fuel = math.floor(mass // 3) - 2
  cache[mass] = fuel + calculateFuel(fuel)
  return cache[mass]
  
"""
print(calculateFuel(14))
print(calculateFuel(1969))
print(calculateFuel(100756))
"""
with open("1.in") as input: 
  s = 0
  for line in input:
    s += calculateFuel(int(line))

  print(s)