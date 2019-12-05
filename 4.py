def has_double(number_str):
    for i in range(len(number_str) - 1):
        if number_str[i] == number_str[i + 1]:
            return True
    return False


def has_double2(number_str):
    # computer a hoffman encoding
    runs = []
    run_number = None
    run_count = 0
    for n in number_str:
        if run_number is None:
            run_number = n
            run_count = 1
        elif run_number == n:
            run_count += 1
        else:
            runs.append((run_number, run_count))
            run_number = n
            run_count = 1
    if run_number is not None:
        runs.append((run_number, run_count))
    # see if any run is length 2
    for run in runs:
        if run[1] == 2:
            return True
    return False


def always_increasing(number_str):
    for i in range(1, len(number_str)):
        if number_str[i] < number_str[i - 1]:
            return False
    return True


def is_password(number_str):
    return has_double2(number_str) and always_increasing(number_str)


"""
print(is_password("11111111"))
print(is_password("223450"))
print(is_password("123789"))
print(is_password("123444"))
print(is_password("1234444"))
print(is_password("111122"))
"""

count = 0
for x in range(273025, 767253):
    if is_password(str(x)):
        count += 1

print(count)

