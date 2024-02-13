def read_bits(filename):

    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    i = 0
    while i < len(lines):
        lines[i] = lines[i].strip()
        i = i + 1

    return lines


def format_bits(lines, expected_length):

    lines_copy = lines

    if not len(lines):
        lines.append("0")

    i = 0
    while i < len(lines):
        temp = list(lines[i])
        temp.reverse()

        while len(temp) < expected_length:
            temp.append("0")

        while len(temp) > expected_length:
            temp.pop()

        temp.reverse()
        lines_copy[i] = temp

        i = i + 1

    return lines_copy


def convert_bits(lines):

    lines_copy = lines

    i = 0
    while i < len(lines_copy):
        j = 0
        while j < len(lines_copy[i]):
            if lines_copy[i][j] == "0":
                lines_copy[i][j] = False
            else:
                lines_copy[i][j] = True
            j = j + 1
        i = i + 1

    return lines_copy


def complete_read(filename, expected_length):
    return convert_bits(format_bits(read_bits(filename), expected_length))
