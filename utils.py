import sys


# Read from the target input file.
def read_input_file():
    # get file name from command arguments.
    file = sys.argv[1]
    f = open(file, "r")

    base_string_list = []
    index_list1 = []
    index_list2 = []
    is_first_done = False
    for line in f.readlines():
        line = line.strip()
        if not line.isnumeric():
            base_string_list.append(line)
            if len(base_string_list) == 2:
                is_first_done = True
        else:
            if not is_first_done:
                index_list1.append(int(line))
            else:
                index_list2.append(int(line))
    f.close()
    return base_string_list, index_list1, index_list2


# return 2 generated lists.
def string_generator_wrapper():
    base_string_list, index_list1, index_list2 = read_input_file()
    result = [string_generator(index_list1, base_string_list[0]), string_generator(index_list2, base_string_list[1])]
    return result


# logic to generate new strings.
def string_generator(index_list, base_string):
    index = 0
    while index < len(index_list):
        base_string = base_string[0:index_list[index] + 1] + base_string + base_string[index_list[index] + 1:]
        index += 1
    return base_string


# function to write new string to strings.txt file.
def save_generated_strings():
    result = string_generator_wrapper()
    file = open("strings.txt", 'wt')
    file.write('\n'.join(result))
    file.close()
    return result
