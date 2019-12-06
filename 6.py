star_map = {}
cache = {}


def number_of_ancestors(star_map, satellite, cache):
    if satellite in cache:
        return cache[satellite]
    if satellite not in star_map:
        cache[satellite] = 0
    else:
        cache[satellite] = (
            sum(
                map(
                    lambda t: number_of_ancestors(star_map, t, cache),
                    star_map[satellite],
                )
            )
            + 1
        )
    return cache[satellite]


with open("6.in") as input:
    for line in input:
        main, satellite = line.strip().split(")")
        if satellite not in star_map:
            star_map[satellite] = main

"""
count = 0
for s in star_map:
    count += number_of_ancestors(star_map, s, cache)

print(count)
"""


def jumps_to_ancestors(star_map, satellite, terminator, cache):
    if satellite in cache:
        return cache[satellite]
    if satellite not in star_map or satellite == terminator:
        cache[satellite] = 0
    else:
        cache[satellite] = 1 + jumps_to_ancestors(
            star_map, star_map[satellite], terminator, cache
        )
    return cache[satellite]


visited = set()


def find_first_common_ancestor(star_map, a, b, visited):
    while a in star_map or b in star_map:
        if a in visited:
            return a
        if b in visited:
            return b
        visited.add(a)
        visited.add(b)
        a = star_map[a]
        b = star_map[b]
    return None


"""
print(find_first_common_ancestor(star_map, "YOU", star_map["san"], visited))
print(jumps_to_ancestors(star_map, "YOU", "d", cache))
print(jumps_to_ancestors(star_map, star_map["san"], "d", cache))
"""
a = "YOU"
b = "SAN"
common = find_first_common_ancestor(star_map, a, star_map[b], visited)
print(
    jumps_to_ancestors(star_map, star_map[a], common, cache)
    + jumps_to_ancestors(star_map, star_map[b], common, cache)
)

