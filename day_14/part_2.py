input_file = 'puzzle_input.txt'
f = open(input_file).read().strip()


def tilt_platform(platform, direction):
    if direction == 'north':
        for i in range(len(platform)):
            for j in range(len(platform[0])):
                if platform[i][j] == 'O':
                    for k in range(i-1, -1, -1):
                        if platform[k][j] == '#':
                            break
                        elif platform[k][j] == '.':
                            platform[k][j] = 'O'
                            platform[k+1][j] = '.'
                    else:
                        platform[0][j] = '.'
    elif direction == 'west':
        for i in range(len(platform)):
            for j in range(len(platform[0])):
                if platform[i][j] == 'O':
                    for k in range(j-1, -1, -1):
                        if platform[i][k] == '#':
                            break
                        elif platform[i][k] == '.':
                            platform[i][k] = 'O'
                            platform[i][k+1] = '.'
                    else:
                        platform[i][0] = '.'
    elif direction == 'south':
        for i in range(len(platform)-1, -1, -1):
            for j in range(len(platform[0])):
                if platform[i][j] == 'O':
                    for k in range(i+1, len(platform)):
                        if platform[k][j] == '#':
                            break
                        elif platform[k][j] == '.':
                            platform[k][j] = 'O'
                            platform[k-1][j] = '.'
                    else:
                        platform[-1][j] = '.'
    elif direction == 'east':
        for i in range(len(platform)):
            for j in range(len(platform[0])-1, -1, -1):
                if platform[i][j] == 'O':
                    for k in range(j+1, len(platform[0])):
                        if platform[i][k] == '#':
                            break
                        elif platform[i][k] == '.':
                            platform[i][k] = 'O'
                            platform[i][k-1] = '.'
                    else:
                        platform[i][-1] = '.'
    return platform


def plat_to_string(platform):
    return 'y'.join(['x'.join(x) for x in platform])


def string_to_plat(string):
    return [x.split('x') for x in string.split('y')]


platform = [['#'] + list(x) + ['#'] for x in f.strip().split('\n')]
platform.insert(0, ['#']*len(platform[0]))
platform.append(['#']*len(platform[0]))
size = len(platform)

stored_states = [plat_to_string(platform)]
while True:
    platform = tilt_platform(platform, 'north')
    platform = tilt_platform(platform, 'west')
    platform = tilt_platform(platform, 'south')
    platform = tilt_platform(platform, 'east')
    if plat_to_string(platform) in stored_states:
        break
    stored_states.append(plat_to_string(platform))

first_occurence = stored_states.index(plat_to_string(platform))
cycles = len(stored_states) - first_occurence
platform = string_to_plat(
    stored_states[(1000000000 - first_occurence) % cycles + first_occurence])

print('Day 14 Part 2:', sum(
    [sum([1 for x in p if x == 'O'])*(i) for i, p in enumerate(platform[::-1])]))
