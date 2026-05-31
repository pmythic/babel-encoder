import math

def tostr(bigint):
    if bigint == 0:
        return "0"

    digits = []
    while bigint > 0:
        digits.append(chr(ord('0') + bigint % 10))
        bigint //= 10

    digits.reverse()
    return "".join(digits)

# Based on the exposition and Python implementation by Nick Craig-Wood:
# https://www.craig-wood.com/nick/articles/pi-chudnovsky/
#
# The underlying mathematical formula is the Chudnovsky algorithm
# (Chudnovsky brothers, 1988), derived from Ramanujan-type series.
#
# This implementation has been adapted/modified for use in this project.
def pi_chudnovsky(digits=100):
    """
    Calculate pi using Chudnovsky's series
    """
    one= 10**digits

    k = 1
    a_k = one
    a_sum = one
    b_sum = 0
    C = 640320
    C3_OVER_24 = C**3 // 24
    while True:
        a_k *= -(6*k-5)*(2*k-1)*(6*k-1)
        a_k //= k*k*k*C3_OVER_24
        a_sum += a_k
        b_sum += k * a_k
        k += 1
        if a_k == 0:
            break
    total = 13591409*a_sum + 545140134*b_sum
    pi = (426880*math.isqrt(10005 * one * one)*one) // total
    p = tostr(pi)
    return f"{p[0]}.{p[1:]}"
