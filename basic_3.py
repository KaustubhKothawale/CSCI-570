import time
import psutil

from utils import save_generated_strings

# define penalty values.
alpha_matrix = [[0, 110, 48, 94],
                [110, 0, 118, 48],
                [48, 118, 0, 110],
                [94, 48, 110, 0]]
delta = 30


def mismatch_cost(letter1, letter2):
    allowed_characters = "ACGT"
    index_1, index_2 = allowed_characters.find(letter1), allowed_characters.find(letter2)
    # find mismatch cost.
    return alpha_matrix[index_1][index_2]


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


def get_optimal_path(minimum_cost_dp, s1, s2):
    # initialize function variables.
    i = len(s1)
    j = len(s2)
    s1_final = ''
    s2_final = ''

    # initialise path matrix.
    path = [[0 for c in range(j + 1)] for r in range(i + 1)]
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

    x, y = 0, 0
    len_s1, len_s2 = len(s1), len(s2)
    while x != len_s1 and y != len_s1:
        if x != len_s1 and path[x + 1][y] == 1:
            s1_final = s1_final + s1[x]
            s2_final = s2_final + '_'
            x += 1
        elif y != len_s2 and path[x][y + 1] == 1:
            s1_final = s1_final + '_'
            s2_final = s2_final + s2[y]
            y += 1
        else:
            s1_final = s1_final + s1[x]
            s2_final = s2_final + s2[y]
            x += 1
            y += 1

    if len(s1_final) < 100:
        result_object = [s1_final, s2_final]
    else:
        # didn't understand why this, will figure out tomorrow.
        # result_object = [s1_final[0:50] + " " + s1_final[-50:], s2_final[0:50] + " " + s2_final[-50:]]
        result_object = [s1_final, s2_final]

    return result_object


def basic_sequence_alignment():
    with open("strings.txt", 'r') as input_strings:
        string1 = input_strings.readline().strip()
        string2 = input_strings.readline().strip()

        minimum_cost_dp = calculate_alignment_dp(string1, string2)
        optimal_value = str(minimum_cost_dp[len(string1)][len(string2)])
        optimal_alignments = get_optimal_path(minimum_cost_dp, string1, string2)
        result = [optimal_value]
        result.extend(optimal_alignments)
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
    file = open("output_basic.txt", 'wt')
    file.write('\n'.join(result))
    file.close()


basic_sequence_alignment_wrapper()
