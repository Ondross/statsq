from argparse import ArgumentParser
import matplotlib.pyplot as plt
import random

import correlation as corr

OPTIONS = [-1, 1]  # Possible Y values.


def newData(options, n):
    return [random.choice(options) for i in range(n)]


def showData(dataA, dataB):

    # copy data for editing.
    dataA = list(dataA)
    dataB = list(dataB)
    if len(dataA) != len(dataB):
        raise ValueError("Datasets must be equal length")

    xs = range(len(dataA)+1)
    fig = plt.figure()

    # Create simple axes and define their size.
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_ylim(ymin=min(dataA+dataB)-1, ymax=max(dataA+dataB)+1)

    # Offset data for visibility
    dataA = [x + abs(x/50.0) for x in dataA]
    xs2 = [x+.05 for x in xs]
    xs2[-1] -= .05

    # Duplicate first point, to create a horizontal line.
    dataA.insert(0, dataA[0])
    dataB.insert(0, dataB[0])

    # Show data as step functions.
    ax.step(xs, dataA, color="g")
    ax.step(xs2, dataB, color="b")
    ax.grid()
    ax.set_yticks((-1, 1))

    # Non-blocking.
    plt.draw()


class Correlation(object):
    """
    Two datasets and their correlation.
    """

    def __init__(self, dataA, dataB):
        self.dataA = dataA
        self.dataB = dataB
        self.coefficient = None
        self.offset = None

    def calcCorrelation(self):
        """
        Calls the binary correlation algorithm and selects the correlation
        with the optimal offset.
        """
        potential = corr.calcCorrelates(self.dataA, self.dataB)
        maxCorrelation = (0, 0)
        for correlation in potential:
            if abs(correlation[1]) > abs(maxCorrelation[1]):
                maxCorrelation = correlation
        self.coefficient = maxCorrelation[1]
        self.offset = maxCorrelation[0]


if __name__ == "__main__":
    parser = ArgumentParser("usage: %prog [options]")
    parser.add_argument("-n",
                        dest="numDatasets",
                        default=100,
                        type=int,
                        help="Number of random datasets to test.")
    parser.add_argument("-l",
                        dest="length",
                        default=20,
                        type=int,
                        help="Number of each dataset.")
    args = parser.parse_args()

    datasets = [newData(OPTIONS, args.length) for x in range(args.numDatasets)]

    # Correlate every pair.
    correlations = []
    for idxi, i in enumerate(datasets):
        for idxj, j in enumerate(datasets):

            # Ignore duplicates.
            if idxi > idxj:
                c = Correlation(i, j)
                c.calcCorrelation()
                correlations.append(c)

    # Sort based on max correlation.
    correlations.sort(key=lambda x: abs(x.coefficient), reverse=True)

    # Plot top five correlations.
    for c in correlations[0:5]:
        showData(c.dataA, c.dataB)
        print c.coefficient, c.offset

    # Blocking call to Matplotlib so program doesn't quit.
    plt.show()
