import time
import psutil
import sys

from utils import save_generated_strings

# define penalty values.
mismatch_cost_matrix = [[0, 110, 48, 94],
                        [110, 0, 118, 48],
                        [48, 118, 0, 110],
                        [94, 48, 110, 0]]
delta = 30
output_file_path = file = sys.argv[2]


def mismatch_cost(letter1, letter2):
    allowed_characters = "ACGT"
    index_1, index_2 = allowed_characters.find(letter1), allowed_characters.find(letter2)
    # find mismatch cost.
    return mismatch_cost_matrix[index_1][index_2]


def calculate_alignment_dp(s1, s2):
    len_s1 = len(s1)
    len_s2 = len(s2)

    # initialize dp matrix
    minimum_cost_dp = [[0 for c in range(len_s2 + 1)] for r in range(len_s1 + 1)]
    for i in range(len_s1 + 1):
        minimum_cost_dp[i][0] = delta * i

    for j in range(len_s2 + 1):
        minimum_cost_dp[0][j] = delta * j

    # filling dp matrix
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                minimum_cost_dp[i][j] = min(minimum_cost_dp[i - 1][j - 1],
                                            minimum_cost_dp[i - 1][j] + delta,
                                            minimum_cost_dp[i][j - 1] + delta)
            else:
                minimum_cost_dp[i][j] = min(minimum_cost_dp[i - 1][j - 1] + mismatch_cost(s1[i - 1], s2[j - 1]),
                                            minimum_cost_dp[i - 1][j] + delta, minimum_cost_dp[i][j - 1] + delta)

    return minimum_cost_dp


def get_optimal_path(minimum_cost_dp, string1, string2):
    # initialize function variables.
    x, y = 0, 0
    len_s1, len_s2 = len(string1), len(string2)
    i, j = len(string1), len(string2)
    first_alignment = ''
    second_alignment = ''

    # initialise path matrix.
    path = [[0 for c in range(j + 1)] for r in range(i + 1)]

    # set initial and last element to be included.
    path[i][j] = 1
    path[0][0] = 1

    while i != 0 or j != 0:
        if minimum_cost_dp[i][j] == minimum_cost_dp[i - 1][j] + delta:
            path[i - 1][j] = 1
            i -= 1
        elif minimum_cost_dp[i][j] == minimum_cost_dp[i][j - 1] + delta:
            path[i][j - 1] = 1
            j -= 1
        else:
            path[i - 1][j - 1] = 1
            i -= 1
            j -= 1

    while x != len_s1 and y != len_s1:
        if x != len_s1 and path[x + 1][y] == 1:
            # include character from first and gap at second.
            first_alignment = first_alignment + string1[x]
            second_alignment = second_alignment + '_'
            x += 1
        elif y != len_s2 and path[x][y + 1] == 1:
            # include character from second and gap at first.
            first_alignment = first_alignment + '_'
            second_alignment = second_alignment + string2[y]
            y += 1
        else:
            # both to be included (either same or with mismatch penalty).
            first_alignment = first_alignment + string1[x]
            second_alignment = second_alignment + string2[y]
            x += 1
            y += 1

    return [first_alignment, second_alignment]


def basic_sequence_alignment():
    with open("strings.txt", 'r') as input_strings:
        string1 = input_strings.readline().strip()
        string2 = input_strings.readline().strip()
        # calculate dp matrix for min cost
        minimum_cost_dp = calculate_alignment_dp(string1, string2)
        optimal_value = str(minimum_cost_dp[len(string1)][len(string2)])
        # get optimal alignment sequences.
        optimal_alignments = get_optimal_path(minimum_cost_dp, string1, string2)
        result = [optimal_value]
        result.extend(optimal_alignments)
        # return optimal alignments with optimal cost.
        return result


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def time_wrapper():
    start_time = time.time()
    save_generated_strings()
    result = basic_sequence_alignment()
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    result.append(str(time_taken))
    return result


def basic_sequence_alignment_wrapper():
    result = time_wrapper()
    result.append(str(process_memory()))
    file_object = open(output_file_path, 'wt')
    file_object.write('\n'.join(result))
    file_object.close()


basic_sequence_alignment_wrapper()
