def miller_rabin(n, k):
    """
    Miller Rabin primality test for n
    Will fail when n is a carmichael number
    :param n: an integer greater than 1
    :param k: number of random trials
    :return: True if "probably prime", False otherwise
    """
    if n % 2 == 0:  # return false if even number
        return False
    elif n == 2 or n == 3:
        return True

    # First factorise n-1
    s = 0
    t = n - 1
    while t % 2 == 0:
        t = t//2
        s += 1

    for i in range(k):
        a = rnd.randrange(2, n-1)

        #if fast_expo(a, n-1, n) != 1:
        if pow(a, n-1, n) != 1:
            return False
        else:
            #old = fast_expo(a, t, n)  # get a^((2^0)*t) first
            old = pow(a, t, n)
            for j in range(1, s):
                new = pow(old, 2, n)
                if new == 1 and (old != n-1 and old != 1):
                    return False
                else:
                    old = new

    return True  # Finally passed all the tests so probably prime
