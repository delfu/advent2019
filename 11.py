from IntCodes import IntCodes


def parse_input():
    program = []
    with open("11.in") as input:
        for line in input:
            line = line.strip().split(",")
            program += list(map(int, line))
    return program


def run(input=[0]):
    program = parse_input()
    runner = IntCodes()

    grid = {}
    pos = (0, 0)
    direction = 0  # 0,1,2,3 = up,right,down,left
    process = runner.run_program(program, input)
    while True:
        try:
            color = next(process)
            rotation = "left" if next(process) == 0 else "right"
            grid[pos] = color
            if rotation == "left":
                direction = (direction - 1) % 4
            else:
                direction = (direction + 1) % 4

            # move robot
            if direction == 0:
                pos = (pos[0], pos[1] - 1)
            elif direction == 1:
                pos = (pos[0] + 1, pos[1])
            elif direction == 2:
                pos = (pos[0], pos[1] + 1)
            elif direction == 3:
                pos = (pos[0] - 1, pos[1])

            new_color = 0 if pos not in grid else grid[pos]
            input.append(new_color)

            if color is None or rotation is None:
                break
        except StopIteration:
            break
    return grid


def print_grid(grid):
    # print(grid, len(grid))
    x_values = set([k[0] for k in grid.keys()])
    y_values = set([k[1] for k in grid.keys()])
    min_y = min(y_values)
    min_x = min(x_values)
    num_col = len(x_values)
    num_row = len(y_values)

    output = [[0 for i in range(num_col)] for j in range(num_row)]
    for key in grid:
        x, y = key
        x -= min_x
        y -= min_y
        output[y][x] = grid[key]

    with open("11.out", "w") as outfile:
        for row in output:
            for cell in row:
                outfile.write(" ") if cell == 0 else outfile.write("X")
            outfile.write("\n")


grid = run([1])
print_grid(grid)
