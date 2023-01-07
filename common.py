import sys
from math import floor
from os import path

TEST_ROWS = 5000
MINUTES_PER_DAY = 24 * 60
MIN_OFFSET = 1
KEY_FLAG = 'flag'
FLAG_POSITIVE = 1
FLAG_NEGATIVE = 0
BASE_DIR = path.dirname(__file__)


def relative_path(p):
    '''
    Returns `path.join(BASE_DIR, p)`.
    '''
    return path.join(BASE_DIR, p)


def offset2days(offset):
    return floor(offset / MINUTES_PER_DAY)


def mean(values):
    count = len(values)
    if count == 0:
        return np.nan
    else:
        return sum(values) / count


class SimpleProgress:

    fmt: str

    def __init__(self, values, fmt='{:.0%}'):
        self.values = list(values)
        self.fmt = fmt
        self.n = len(self.values)
        self.i = 0
        self.last_output = None

    def __iter__(self):
        return self

    def __next__(self):
        n = self.n
        i = self.i
        if i == n:
            sys.stdout.write('\n')
            raise StopIteration()
        else:
            pct = (i + 1) / n
            output = self.fmt.format(pct)
            if output != self.last_output:
                self.last_output = output
                if i > 0:
                    sys.stdout.write('\r')
                sys.stdout.write(output)
                sys.stdout.flush()
            self.i += 1
            return self.values[i]
