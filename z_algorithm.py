def z_algorithm(pattern):
    """
    Computes the the z-values for an input pattern
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
