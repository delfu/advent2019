n = 25
m = 6

with open("8.in") as input:
    line = input.readline().strip()
    layers = []
    counter = {}
    layer = ""
    for i, pixel in enumerate(line):
        if i % (n * m) == 0:
            layers.append(layer)
            layer = ""
        layer += pixel
    layers.append(layer)
    layers = layers[1:]

    target_layer = None
    least_0 = 9999999999999999999
    for layer in layers:
        count_0 = sum([1 if p == "0" else 0 for p in layer])
        if count_0 < least_0:
            least_0 = count_0
            target_layer = layer
    count_1 = 0
    count_2 = 0
    count_1 = sum([1 if p == "1" else 0 for p in target_layer])
    count_2 = sum([1 if p == "2" else 0 for p in target_layer])

    print(count_1 * count_2)

    visible_layer = ""
    for i in range(n * m):
        for layer in layers:
            if layer[i] == "0" or layer[i] == "1":
                visible_layer += layer[i]
                break
    with open("8.out", "w") as output:
        for i, p in enumerate(visible_layer):
            if i % n == 0:
                output.write("\n")
            output.write(" ") if p == "0" else output.write("x")

