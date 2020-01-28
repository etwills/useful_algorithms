def boyer_moore(text, pattern):
    """
    The boyer moore string match algorithm
    Assumes the strings contain only ascii characters

    :param pattern:  a string of length m
    :param text: a string of length n >= m
    :return: matches a set of indexes where matches occur
    """


    # preprocess pattern
    # check for matchs
    # find length of jump with bad character
    # find length with good suffix
    # Shift with best

    preprop = preprocess(pattern)
    bc_shift = preprop[0]
    gs_shift = preprop[1]

    matches = set()

    index = 0
    while (index + len(pattern)) <= len(text):
        k = len(pattern) - 1
        is_match = True
        while k >= 0:
            if pattern[k] != text[index + k]:
                # determine max shift from bad character rule and good suffix rule
                # BC rule
                char_index = ord(text[index+ k])
                most_left_occ = bc_shift[k][char_index]

                if most_left_occ == -1:
                    bc_shift_amount = k + 1
                else:
                    bc_shift_amount = k - most_left_occ

                if gs_shift[k-1]>0:
                    gs_shift_amount = len(pattern) - gs_shift[k-1]
                else:
                    gs_shift_amount = 1


                shift_amount = max(1, gs_shift_amount, bc_shift_amount)
                index += shift_amount


                is_match = False
                break
            else:
                k -= 1

        if is_match:
            matches.add(index)
            index += 1

    return matches



def preprocess2D(pattern):
    """

    alphabet = ascii
    Table is length of pattern * 128. First index is position of pattern, next is location of letter

    :param pattern: the pattern to be analysed
    :return:  Bad character shift table
    """

    locations = [None]*len(pattern)  #Length of ascii
    for k in range(len(pattern)):
        locations[k] = [-1] * 128



    #set first character
    index = ord(pattern[0])
    locations[0][index] = 0

    #Now do the rest of the rows
    for k in range(1,len(pattern)):
        for i in range(128):
            if pattern[k] == chr(i):
                locations[k][i] = k
            else:
                locations[k][i] = locations[k-1][i]
    return locations





def preprocess(pattern):

    """
    All preprocessing for boyer-moore
    :param pattern:
    :return:
    """

    bc_table = preprocess2D(pattern)
    gc_array = good_suffix(pattern)
    return [bc_table, gc_array]


def good_suffix(pattern):
    """
    Computes the good suffix of
    :param pattern: the string to compute good suffix
    :return: Array of good suffix
    """

    rev_pattern = ''
    for i in range(len(pattern)):
        rev_pattern += pattern[i]
    reversed(rev_pattern)
    z_suffix_array = z_algorithm(rev_pattern)
    reversed(z_suffix_array)

    gs_array = [0]*len(pattern)
    for p in range(len(pattern) - 2):
        j = len(pattern)-1 - (gs_array[p])
        gs_array[j] = p

    return gs_array


def partition(string):
    """
    A function to partition string into 2 pieces

    :param string: a string
    :return: An array with partitions of string
    """
    n = len(string)
    center = math.floor(n/2)
    part1 = ""
    for i in range(center):
        part1 += string[i]
    part2 = ""
    for i in range(center, n):
        part2 += string[i]

    return [part1, part2]



def z_algorithm(pattern):
    """
    :param string: a string to compute the z_values assumed longer than 2
    :return: z_values of string
    """
    string = pattern
    if len(string) <= 1:
        return[1]

    #first Z2
    z_array = [0]* len(string)
    z_array[0] = None

    r = 0
    l = 0
    i = 0
    while string[i] == string[1+i]:
        i += 1
        if i+1 >= len(string):
            break

    if i > 0:
        z_array[1] = i
        l = 1
        r = i

    k = 2
    while k < len(string):
        if k > r:
            i = 0
            while string[i] == string[i + k]:
                i += 1
                if i+k >= len(string):
                    break

            z_array[k] = i
            if i > 0:
                l = k
                r = k + i - 1

        elif k <= r:    #we are in the z-box
            if z_array[k-l] < r - k + 1:
                z_array[k] = z_array[k-l]

            else:# z_array[k-l] >= r - k + 1
                if r+1 < len(string):       #We can look for letters after with z_box
                    i = 0
                    while string[r - k + i + 1] == string[r + i + 1]:
                        i += 1
                        if i + r + 1 >= len(string):
                            break

                    #we have i matches after
                    if i > 0:
                        z_array[k] = r - k + 1 + i
                        l = k
                        r = r + i
                    else:
                        z_array[k] = r - k + 1

                else: #we have to have that z_array[k] = r-k+1
                    z_array[k] = r-k+1

        k += 1
    return z_array


def process_text(input_text):
    """
    Function to process the input text
    :param input_text: a text file according to assignment specs with text
    :return: text_string, the text
    """
    text = open(input_text, 'r')
    text_string = text.read()
    text.close()
    return text_string


def process_pattern(input_pattern):
    """
    Function to process the input text
    :param input_pattern: a text file according to assignment specs with pattern
    :return: pattern_string, the pattern
    """
    pattern = open(input_pattern, 'r')
    pattern_string = pattern.read()
    pattern.close()
    return pattern_string
