
import numpy as np
import matplotlib.pyplot as plt
from contextlib import contextmanager

from dice_tower.dice import main

import os
import sys


# Display Infrastructure
def graph(values, name):
    # Histogram of data
    values = np.array(values).flatten()

    plt.hist(values)

    plt.xlabel('Value')
    plt.ylabel('Probability')
    plt.title('Histogram of Dice Roll')
    plt.savefig(name+'.png')


def display(s, amount=20):
    # Show a sample distribution
    v = []
    args = EmulatedArg(s)
    for n in range(amount):
        v.append(main(args))

    graph(v, s)
    return v


# Test Infrastructure

def spread(s, fail=False):

    v = []
    l = testLow(s)
    h = testHigh(s)

    v.append(l)
    v.append(h)

    isInt = True
    try:
        vts = []
        vts.append(int(v[0]))
        vts.append(int(v[1]))
    except (TypeError, ValueError):
        isInt = False
        v[0] = v[0] if isinstance(v[0], list) else [v[0]]
        v[1] = v[1] if isinstance(v[1], list) else [v[1]]

    if isInt:
        vs = np.arange(vts[0], vts[1]+1)
        return vs
    else:
        return list(v)


class EmulatedArg():
    def __init__(self, s, verbose=False, silent=True, hi=False, lo=False, macro=True):
        self.roll_string = s
        self.verbose = verbose
        self.silent = silent
        self.force_max = hi
        self.force_min = lo
        self.macros = macro


def testHigh(s):
    a = EmulatedArg(s, hi=True)
    return main(a)


def testLow(s):
    a = EmulatedArg(s, lo=True)
    return main(a)


def check_values(roll_text, lowest=0, highest=0, debug=False):

    data = spread(roll_text)

    isInt = True
    try:
        l = int(lowest)
        h = int(highest)
        lowest = l
        highest = h
    except (TypeError, ValueError):
        isInt = False

    if isInt:
        expected = np.arange(lowest, highest+1)
    else:
        lowest = str(lowest).strip().replace("\"", "")
        highest = str(highest).strip().replace("\"", "")

        if ":" in lowest or ":" in highest:
            # Sequence
            lowest = [x for x in lowest.split(":")]
            highest = [x for x in highest.split(":")]

            try:
                lowestInt = [int(x) for x in lowest]
                highestInt = [int(x) for x in highest]
                lowest = lowestInt
                highest = highestInt
            except (TypeError, ValueError):
                pass

        lowest = lowest if isinstance(lowest, list) else [lowest]
        highest = highest if isinstance(highest, list) else [highest]

        expected = [lowest, highest]

    # debug = True
    if debug:
        print("CMP:", data, expected)

    return np.array_equal(data, expected), data, expected, roll_text


@contextmanager
def suppress_prints():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        old_stdout = sys.stdout
        sys.stderr = devnull
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr
            sys.stdout = old_stdout