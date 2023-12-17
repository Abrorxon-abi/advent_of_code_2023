HORIZONTAL = 0
VERTICAL = 1


def find_horizontal_reflection(reflection):
    answers = []
    for idx, line in enumerate(reflection):
        if idx < len(reflection) - 1:
            next_line = reflection[idx + 1]
            if line == next_line:
                if is_actual_reflection(reflection, idx, idx + 1):
                    answers.append(idx + 1)

    return answers


def is_actual_reflection(reflection, l1, l2):
    check = 1
    reflection_reaches_edge = True
    while True:
        c1 = l1 - check
        c2 = l2 + check

        if c1 < 0 or c2 == len(reflection):
            break

        if reflection[c1] != reflection[c2]:
            reflection_reaches_edge = False
            break

        check += 1

    if reflection_reaches_edge:
        return True
    else:
        return False


def find_vertical_reflection(reflection):
    rotated_reflection = rotate_reflection(reflection)

    return find_horizontal_reflection(rotated_reflection)


def find_reflection(reflection):
    h_answers = find_horizontal_reflection(reflection)
    v_answers = find_vertical_reflection(reflection)
    if h_answers:
        return HORIZONTAL, h_answers
    else:
        return VERTICAL, v_answers


def rotate_reflection(reflection):
    rotated_reflection = []

    for x in range(len(reflection[0])):
        line = ""
        for y in range(len(reflection) - 1, -1, -1):
            line += reflection[y][x]
        rotated_reflection.append(line)

    return rotated_reflection


def find_reflection_with_smudge(reflection):
    orig_dir, answers = find_reflection(reflection)
    orig_answer = answers[0]

    for y in range(len(reflection)):
        for x in range(len(reflection[0])):
            reflection_copy = reflection.copy()
            line = reflection_copy[y]
            c = line[x]
            if c == ".":
                line = line[:x] + "#" + line[x + 1:]
            else:
                line = line[:x] + "." + line[x + 1:]

            reflection_copy[y] = line

            h_answers, v_answers = find_all_reflections(reflection_copy)

            if orig_dir == HORIZONTAL:
                h_answers = [
                    answer for answer in h_answers if answer != orig_answer]
            else:
                v_answers = [
                    answer for answer in v_answers if answer != orig_answer]

            if not h_answers and not v_answers:
                continue

            if h_answers:
                return HORIZONTAL, h_answers[0]
            else:
                return VERTICAL, v_answers[0]


def find_all_reflections(reflection):
    h_answers = find_horizontal_reflection(reflection)
    v_answers = find_vertical_reflection(reflection)
    return h_answers, v_answers


def read_file(file_name):
    with open(file_name) as f:
        content = f.read().splitlines()
    return content


def parse_input(input_lines):
    reflections = []
    this_reflection = []
    for line in input_lines:
        if line == "":
            reflections.append(this_reflection.copy())
            this_reflection = []
        else:
            this_reflection.append(line)

    reflections.append(this_reflection.copy())
    return reflections


input_lines = read_file("puzzle_input.txt")


reflections = parse_input(input_lines)


def calc_answer_for_part_two(reflections):
    answer = 0
    for idx, reflection in enumerate(reflections):
        direction, num = find_reflection_with_smudge(reflection)

        if direction == HORIZONTAL:
            answer = answer + num * 100
        else:
            answer = answer + num

    return answer


part_2_answer = calc_answer_for_part_two(reflections)
print(f"Part 2: {part_2_answer}")
