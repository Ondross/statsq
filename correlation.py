# Algorithm Trial 01

# Purpose: compare 2 signals to find a measure of their correlation
# Method: inspired by cross-correlation.
#     - Multiply of the signals' values at each time step, and sum all the
#       multiples, and normalize (divide by length of vector).
#     - offset how the signals are lined-up by 1, and repeat
#     - the offset that begets the greatest magnitude sum is the offset of
#       greatest signal correlation


import numpy as np


# DEFINE FUNCTION
def calcCorrelates(n1, n2, period=None, maxstep=3):
    """
    For two input vectors n1 and n2 this returns the value of their correlation
    in the timeframe 'period' and for each # days offset up to 'maxstep', in
    the format of a list of (offset, correlation_coefficient)
    """
    # period = period (range of timesteps) from signals to use in comparison. i.e. looks back 5 days
    # maxstep = max offset to compare signals
    if period:
        start = len(n1)-period
    else:
        start = 0
    endd = len(n1)
    vals = []  # list of (time offset, correlation value)

    for tstep in range(0, maxstep):
        n12 = []
        for x in range(start, endd):
            n12.append(float(n1[x-tstep]*n2[x]))
        corr = sum(n12)/len(n12)
        vals.append((tstep, corr))
    return vals


if __name__ == "__main__":

    # 1. EXAMPLE VECTORS. Each input signal is a vector of integer (& binary, to start) values.
    A = [-1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1]
    B = A
    C = [-1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1]  # =A delayed 1 timestep
    D = [x*-1 for x in A]  # = -A

    # 2. CALCULATE CORRELATION
    vals = calcCorrelates(A, C)
    print vals
