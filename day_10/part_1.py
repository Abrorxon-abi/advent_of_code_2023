import math

f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

coords = [0, 0]
for i, x in enumerate(lines):
    if "S" in x:
        coords[0] = i
        coords[1] = x.index("S")


direction = 0
steps = 0
currTile = lines[coords[0]][coords[1]]
while (True):
    steps += 1
    match currTile:
        case "|" | "S":
            if direction == 0:
                coords[0] -= 1
            else:
                coords[0] += 1
        case "-":
            if direction == 2:
                coords[1] += 1
            else:
                coords[1] -= 1
        case "L":
            if direction == 1:
                coords[1] += 1
                direction = 2
            else:
                coords[0] -= 1
                direction = 0
        case "J":  # ┘ should"ve been better
            if direction == 1:
                coords[1] -= 1
                direction = 3
            else:
                coords[0] -= 1
                direction = 0
        case "7":  # ┐
            if direction == 0:
                coords[1] -= 1
                direction = 3
            else:
                coords[0] += 1
                direction = 1
        case "F":  # ┌
            if direction == 0:
                coords[1] += 1
                direction = 2
            else:
                coords[0] += 1
                direction = 1
        case _:
            print("?")
    currTile = lines[coords[0]][coords[1]]
    if (currTile == "S" or currTile == '.'):
        break

print(math.ceil(steps/2))
