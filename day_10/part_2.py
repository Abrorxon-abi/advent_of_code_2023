f = open("puzzle_input.txt", "r")
lines = f.read().splitlines()
f.close()

coords = [0, 0]
for i, x in enumerate(lines):
    if "S" in x:
        coords[0] = i
        coords[1] = x.index("S")

pipeMap = [['.']*len(lines[0]) for x in range(len(lines))]

direction = 0
steps = 0
currTile = lines[coords[0]][coords[1]]
while (True):
    steps += 1
    match currTile:
        case "|" | "S":
            if direction == 0:
                pipeMap[coords[0]][coords[1]] = '^'
                coords[0] -= 1
            else:
                pipeMap[coords[0]][coords[1]] = 'v'
                coords[0] += 1
        case "-":
            pipeMap[coords[0]][coords[1]] = '─'
            if direction == 2:
                coords[1] += 1
            else:
                coords[1] -= 1
        case "L":
            if direction == 1:
                pipeMap[coords[0]][coords[1]] = '↳'
                coords[1] += 1
                direction = 2
            else:
                pipeMap[coords[0]][coords[1]] = '└'
                coords[0] -= 1
                direction = 0
        case "J":  # ┘ should"ve been better
            if direction == 1:
                pipeMap[coords[0]][coords[1]] = '↲'
                coords[1] -= 1
                direction = 3
            else:
                pipeMap[coords[0]][coords[1]] = '┘'
                coords[0] -= 1
                direction = 0
        case "7":  # ┐
            pipeMap[coords[0]][coords[1]] = '┐'
            if direction == 0:
                coords[1] -= 1
                direction = 3
            else:
                coords[0] += 1
                direction = 1
        case "F":  # ┌
            pipeMap[coords[0]][coords[1]] = '┌'
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


total = 0
for j, y in enumerate(pipeMap):
    windNum = 0
    for i, x in enumerate(y):
        match x:
            case '^':
                windNum += 1
            case 'v':
                windNum -= 1
            case  '┌' | '┐':
                if (pipeMap[j+1][i] == '└' or pipeMap[j+1][i] == '┘' or pipeMap[j+1][i] == '^'):
                    windNum += 1
                elif (pipeMap[j+1][i] == '↳' or pipeMap[j+1][i] == '↲' or pipeMap[j+1][i] == 'v'):
                    windNum -= 1
            case '.':
                if windNum != 0:
                    total += 1
            case _:
                pass

print(total)
