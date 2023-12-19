input_file = 'puzzle_input.txt'

f = open(input_file).read().strip()

grid = [list(x) for x in f.strip().split('\n')]


def follow_beam(beam_coord, direction, visited_coords):
    if (beam_coord, direction) not in visited_coords:
        visited_coords.add((beam_coord, direction))

    while True:
        if grid[beam_coord[1]][beam_coord[0]] == '.':
            pass
        elif grid[beam_coord[1]][beam_coord[0]] == '/':
            if direction == 'right':
                direction = 'up'
            elif direction == 'left':
                direction = 'down'
            elif direction == 'up':
                direction = 'right'
            elif direction == 'down':
                direction = 'left'
        elif grid[beam_coord[1]][beam_coord[0]] == '\\':
            if direction == 'right':
                direction = 'down'
            elif direction == 'left':
                direction = 'up'
            elif direction == 'up':
                direction = 'left'
            elif direction == 'down':
                direction = 'right'
        elif grid[beam_coord[1]][beam_coord[0]] == '|':
            if direction == 'right':
                visited_coords = follow_beam(beam_coord, 'up', visited_coords)
                direction = 'down'
            elif direction == 'left':
                visited_coords = follow_beam(beam_coord, 'up', visited_coords)
                direction = 'down'
            elif direction == 'up':
                pass
            elif direction == 'down':
                pass
        elif grid[beam_coord[1]][beam_coord[0]] == '-':
            if direction == 'right':
                pass
            elif direction == 'left':
                pass
            elif direction == 'up':
                visited_coords = follow_beam(
                    beam_coord, 'left', visited_coords)
                direction = 'right'
            elif direction == 'down':
                visited_coords = follow_beam(
                    beam_coord, 'left', visited_coords)
                direction = 'right'

        if direction == 'right':
            beam_coord = (beam_coord[0]+1, beam_coord[1])
        elif direction == 'left':
            beam_coord = (beam_coord[0]-1, beam_coord[1])
        elif direction == 'up':
            beam_coord = (beam_coord[0], beam_coord[1]-1)
        elif direction == 'down':
            beam_coord = (beam_coord[0], beam_coord[1]+1)

        if (beam_coord, direction) in visited_coords or beam_coord[0] < 0 or beam_coord[0] >= len(grid[0]) or beam_coord[1] < 0 or beam_coord[1] >= len(grid):
            break
        else:
            visited_coords.add((beam_coord, direction))

    return visited_coords


max_energized = 0
for x in range(len(grid[0])):
    visited_coords = follow_beam((x, 0), 'down', set())
    energized_coords = set([x[0] for x in visited_coords])
    max_energized = len(energized_coords) if len(
        energized_coords) > max_energized else max_energized
for x in range(len(grid[0])):
    visited_coords = follow_beam((x, len(grid)-1), 'up', set())
    energized_coords = set([x[0] for x in visited_coords])
    max_energized = len(energized_coords) if len(
        energized_coords) > max_energized else max_energized
for y in range(len(grid)):
    visited_coords = follow_beam((0, y), 'right', set())
    energized_coords = set([x[0] for x in visited_coords])
    max_energized = len(energized_coords) if len(
        energized_coords) > max_energized else max_energized
for y in range(len(grid)):
    visited_coords = follow_beam((len(grid[0])-1, y), 'left', set())
    energized_coords = set([x[0] for x in visited_coords])
    max_energized = len(energized_coords) if len(
        energized_coords) > max_energized else max_energized

print('Day 16 Part 2:', max_energized)
