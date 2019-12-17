import re
from itertools import combinations
import json


def parse_input(with_energy=True):
    moons = []
    with open("12.in") as input:
        for line in input:
            line = line.strip()
            pos = list(map(int, re.findall("<x=(.*), y=(.*), z=(.*)>", line)[0]))
            vel = [0, 0, 0]
            if with_energy:
                energy = 0
                moons.append({"pos": pos, "vel": vel, "energy": energy})
            else:
                moons.append({"pos": pos, "vel": vel})
    return moons


def step(moons, dim):
    combos = combinations(moons, 2)
    for combo in combos:
        vel = combo[0]["vel"]
        vel2 = combo[1]["vel"]
        pos = combo[0]["pos"]
        pos2 = combo[1]["pos"]
        if pos[dim] < pos2[dim]:
            vel[dim] += 1
            vel2[dim] -= 1
        elif pos[dim] > pos2[dim]:
            vel[dim] -= 1
            vel2[dim] += 1
    for moon in moons:
        vel = moon["vel"]
        pos = moon["pos"]
        pos[dim] = pos[dim] + vel[dim]


def part1():
    moons = parse_input()
    for _ in range(1000):
        step(moons, 0)
        step(moons, 1)
        step(moons, 2)
        print(
            sum(
                map(
                    lambda moon: sum(map(abs, moon["vel"]))
                    * sum(map(abs, moon["pos"])),
                    moons,
                )
            )
        )


def part2():
    def gcd(a, b):
        while b > 0:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return a * b // gcd(a, b)

    moons = parse_input(False)
    cycles = [0, 0, 0]
    seens = [set(), set(), set()]

    for dim in range(3):
        i = 0
        while True:
            step(moons, dim)
            positions = ",".join(map(lambda moon: str(moon["pos"][dim]), moons))
            velocities = ",".join(map(lambda moon: str(moon["vel"][dim]), moons))
            hash = positions + ":" + velocities
            if hash in seens[dim]:
                cycles[dim] = i
                break
            else:
                seens[dim].add(hash)
            i += 1
    print(cycles)
    print(lcm(cycles[0], lcm(cycles[1], cycles[2])))


part2()
