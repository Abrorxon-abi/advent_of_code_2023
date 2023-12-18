num = 0
num_words = ['zero', 'one', 'two', 'three', 'four',
             'five', 'six', 'seven', 'eight', 'nine']

with open("puzzle_input.txt", "r") as file:
    lines = file.readlines()
    for row in lines:
        st = ''
        word = ''
        for item in row:
            if item.isdigit():
                st = st + str(item)
                word = ''
            else:
                word = word + item
                for i in num_words:
                    if i in word:
                        st = st + str(num_words.index(i))
                        word = word[-1]
        if len(st) == 1:
            st = st + st
        if len(st) > 2:
            st = st[0] + st[- 1]
        num = num + int(st)

print('Day 1 Part 2:', num)
