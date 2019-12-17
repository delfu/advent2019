from IntCodes import IntCodes


def parse_input():
    program = []
    with open("13.in") as input:
        for line in input:
            line = line.strip()
            program += list(map(int, line.split(",")))
    return program


def game():
    program = parse_input()
    runner = IntCodes()
    controls = []
    process = runner.run_program(program, controls)

    board = [[0 for i in range(50)] for j in range(20)]
    score = 0
    ball_x = None
    paddle_x = None
    while True:
        try:
            x = next(process)
            y = next(process)
            tile = next(process)

            if x is None or y is None or tile is None:
                break

            if x == -1 and y == 0:
                score = tile
                continue

            if tile == 0:
                board[y][x] = 0
            else:
                board[y][x] = tile
                if tile == 4:
                    ball_x = x
                elif tile == 3:
                    paddle_x = x
            # print_game(board, score)
            if ball_x is not None and paddle_x is not None:
                runner.input = [
                    -1 if ball_x < paddle_x else 1 if ball_x > paddle_x else 0
                ]

        except StopIteration:
            break
    # part 1
    # print(sum([sum([1 if cell == 2 else 0 for cell in row]) for row in board]))
    print(score)
    print_game(board, score)


def print_game(board, score):
    for row in board:
        print(
            "".join(
                [
                    "|"
                    if c == 1
                    else "#"
                    if c == 2
                    else "_"
                    if c == 3
                    else "*"
                    if c == 4
                    else " "
                    for c in row
                ]
            )
        )
    print(score)
    print("======================")


game()
