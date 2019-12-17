from math import gcd
from copy import deepcopy


def LOS_angle(x_start, y_start, x_target, y_target):
    delta_y, delta_x = y_target - y_start, x_target - x_start
    if delta_x == 0:  # same col
        return 0, (1 if delta_y > 0 else -1)
    if delta_y == 0:  # same row
        return (1 if delta_x > 0 else -1), 0
    common = gcd(delta_x, delta_y)
    return delta_x / common, delta_y / common


def print_map(star_map):
    for row in star_map:
        print("".join(row))


puzzle = []
astroids = []
counts = []
m = 0
max_i = 0
with open("10.in") as input:
    for line in input:
        row = list(line.strip())
        puzzle.append(row)

for y, row in enumerate(puzzle):
    for x, cell in enumerate(row):
        if cell == "#":
            astroids.append((x, y))

for i in range(len(astroids)):
    seen = set()
    # star_map = deepcopy(puzzle)
    # star_map[astroids[i][1]][astroids[i][0]] = "O"
    for j in range(len(astroids)):
        if i == j:
            continue
        delta_x, delta_y = LOS_angle(
            astroids[i][0], astroids[i][1], astroids[j][0], astroids[j][1]
        )
        if (delta_x, delta_y) in seen:
            # print("blocked", astroids[i], astroids[j], (delta_x, delta_y))
            continue
        else:
            # star_map[astroids[j][1]][astroids[j][0]] = "X"
            seen.add((delta_x, delta_y))
    # print_map(star_map)
    # print("============", i)
    counts.append(len(seen))
for i in range(len(counts)):
    if counts[i] > m:
        max_i = i
        m = counts[i]
print(astroids[max_i], counts[max_i])


# part two
from math import sqrt, acos, atan2, degrees


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return sqrt(dotproduct(v, v))


def angle(v1, v2):
    v1 = rotate(v1)
    v2 = rotate(v2)
    dot = v1[0] * v2[0] + v1[1] * v2[1]  # dot product
    det = v1[0] * v2[1] - v1[1] * v2[0]  # determinant
    deg = degrees(atan2(det, dot))
    if deg < 0:
        return 360 + deg
    return deg


# we are essentially rotating vectors 90deg
def rotate(v):
    # (0, -1) will be projected to (1, 0) in the unit circle
    # (1, -1) will be projected to (1, -1) in the unit circle
    # (1, 0) will be (0, -1)
    # (0, 1) will be (-1, 0)
    return (v[1], -v[0])


def distance(o_x, o_y, x, y):
    return sqrt((y - o_y) ** 2 + (x - o_x) ** 2)


# # debug only
# max_i = 28
# star_map = deepcopy(puzzle)
# star_map[astroids[max_i][1]][astroids[max_i][0]] = "X"

angle_map = {}
starting = astroids[max_i]
for i in range(len(astroids)):
    if i == max_i:
        continue
    delta_x, delta_y = LOS_angle(
        starting[0], starting[1], astroids[i][0], astroids[i][1]
    )
    entry = (
        astroids[i][0],
        astroids[i][1],
        distance(starting[0], starting[1], astroids[i][0], astroids[i][1]),
    )
    a = angle((0, -1), (delta_x, delta_y))
    if a in angle_map:
        angle_map[a].append(entry)
    else:
        angle_map[a] = [entry]
for angle in angle_map:
    angle_map[angle].sort(key=lambda x: x[2])
sorted_destruction_list = sorted(angle_map.keys())

i = 0
d = 0
# while i < len(astroids) - 1:
while i < 200:
    angle = sorted_destruction_list[d]
    if len(angle_map[angle]) == 0:
        d = (d + 1) % len(sorted_destruction_list)
    else:
        astroid = angle_map[angle].pop(0)
        # star_map[astroid[1]][astroid[0]] = "*"
        # print_map(star_map)
        # print("============", i)
        # star_map[astroid[1]][astroid[0]] = "."
        print(astroid)
        i += 1
        d = (d + 1) % len(sorted_destruction_list)

