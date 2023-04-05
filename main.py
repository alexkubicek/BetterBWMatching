import sys


def add_indices_last(raw):
    last_indices = []
    a = c = t = g = 0
    for char in raw:
        if char == 'A':
            new_char = (char, a)
            a += 1
        elif char == 'C':
            new_char = (char, c)
            c += 1
        elif char == 'T':
            new_char = (char, t)
            t += 1
        elif char == 'G':
            new_char = (char, g)
            g += 1
        else:
            new_char = ('$', 0)
        last_indices.append(new_char)
    return last_indices


def get_counts(lastcol):
    count_dict = dict()
    count_dict['A'] = [0]
    count_dict['C'] = [0]
    count_dict['G'] = [0]
    count_dict['T'] = [0]
    count_dict['$'] = [0]
    for tup in lastcol:
        count_dict['A'].append(count_dict['A'][-1])
        count_dict['C'].append(count_dict['C'][-1])
        count_dict['G'].append(count_dict['G'][-1])
        count_dict['T'].append(count_dict['T'][-1])
        count_dict['$'].append(count_dict['$'][-1])
        count_dict[tup[0]][-1] += 1
    return count_dict


def get_num_matches(last_col, first_o, string):
    top = 0
    bottom = len(last_col)-1
    counts = get_counts(last_col)
    while top <= bottom:
        # print("top: " + str(top) + " bottom: " + str(bottom))
        if len(string) > 0:
            symbol = string[len(string)-1]
            # print(symbol)
            string = string[:len(string)-1]
            if counts[symbol][bottom+1] - counts[symbol][top] > 0:
                top = first_o[symbol] + counts[symbol][top]
                bottom = first_o[symbol] + counts[symbol][bottom+1] - 1
            else:
                return 0
        # print(str(top) + " " + str(bottom))
        else:
            return (bottom - top) + 1
    return 0


def get_first_occurrences(column):
    first_occurrences = {}
    tuples_to_find = [('$', 0), ("A", 0), ('C', 0), ('T', 0), ('G', 0)]
    for tup in tuples_to_find:
        first_occurrences[tup[0]] = column.index(tup)
    return first_occurrences


def better_bwt_matching(bwt, patterns):
    last_column = add_indices_last(bwt)
    first_occurrences = get_first_occurrences(sorted(last_column))
    pattern_matches = []
    for string in patterns:
        pattern_matches.append(get_num_matches(last_column, first_occurrences, string))
    return pattern_matches


if __name__ == '__main__':
    filePath = input()
    inFile = open(filePath)
    file_input = inFile.readline()
    to_match = []
    for line in inFile:
        to_match.extend(line.split(" "))
    while file_input.endswith("\n"):
        file_input = file_input[:len(file_input)-1]
    inFile.close()
    # print(file_input)
    # print(to_match)
    answer = better_bwt_matching(file_input, to_match)
    f = open("output.txt", "w")
    sys.stdout = f
    for num in answer:
        print(num, end=" ")
    f.close()
