from math import inf


def min_distance(grid):
    def distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    min_dist = inf
    for key in grid:
        if grid[key][0] == 3:
            x, y = key.split(":")
            min_dist = min(min_dist, distance(0, 0, int(x), int(y)))
    return min_dist


def min_distance_with_steps(grid):
    min_dist = inf
    for key in grid:
        if len(grid[key]) > 2:
            min_dist = min(min_dist, grid[key][1] + grid[key][2])
    return min_dist


def draw_path(path, grid, curr_ptr, color, acc):
    direction = path[0]
    count = int(path[1:])
    for _ in range(count):
        acc += 1
        if direction == "U":
            curr_ptr[1] -= 1
        elif direction == "D":
            curr_ptr[1] += 1
        elif direction == "L":
            curr_ptr[0] -= 1
        elif direction == "R":
            curr_ptr[0] += 1
        key = str(curr_ptr[0]) + ":" + str(curr_ptr[1])
        if key not in grid:
            grid[key] = [color, acc]
        elif grid[key][0] != color:
            grid[key][0] = color + grid[key][0]
            grid[key].append(acc)
    return grid, curr_ptr, acc


def cross_point(wire1, wire2):
    grid = {}
    starting = [0, 0]
    acc = 0
    wire1 = wire1.strip().split(",")
    wire2 = wire2.strip().split(",")
    for path in wire1:
        grid, starting, acc = draw_path(path, grid, starting, 1, acc)
    starting = [0, 0]
    acc = 0
    for path in wire2:
        grid, starting, acc = draw_path(path, grid, starting, 2, acc)
    # print(min_distance(grid))
    print(min_distance_with_steps(grid))


"""
cross_point("R8,U5,L5,D3", "U7,R6,D4,L4")
cross_point("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83")
cross_point(
    "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
    "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
)

"""
with open("3.in") as input:
    test_case = []
    for line in input:
        line = line.strip()
        test_case.append(line)
    cross_point(test_case[0], test_case[1])

