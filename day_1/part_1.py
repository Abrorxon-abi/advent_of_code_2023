def sum_of_digits(line):
    digits = [char for char in line if char.isdigit()]

    return int(digits[0] + digits[-1])


with open("puzzle_input.txt", "r") as file:
    lines = file.readlines()

final_sum = sum(sum_of_digits(line) for line in lines)
print('Day 01 Part 1:', final_sum)
