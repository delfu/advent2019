def parse_input():
    cases = []
    with open("16.in") as input:
        for line in input:
            cases.append(line.strip())
    return cases


cases = parse_input()


def run_phase(case, phase):
    pattern = [0, 1, 0, -1]
    l = len(case)
    result = [int(case[i]) * pattern[(i + 1) // phase % len(pattern)] for i in range(l)]
    s = sum(result)
    return abs(s) % 10


def run(case):
    next_case = "".join(
        [str(run_phase(case, phase)) for phase in range(1, len(case) + 1)]
    )
    return next_case


def part1():
    case = cases[4]
    num_phase = 100
    for _ in range(num_phase):
        case = run(case)
    print(case[:8])


# part1()
def get_case(case, repeat):
    for i in range(len(case) * repeat):
        yield case[i % len(case)]


def part2():
    case = cases[5]
    offset = int(case[:7])
    num_phase = 100
    for _ in range(num_phase):
        case = run(case)
    print(case[offset : offset + 8])


part1()
