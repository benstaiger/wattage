from functools import reduce
from typing import List, Tuple


class CriticalPower:
    """
    Construct a critical power curve from (seconds, Watts) samples.
    """

    def __init__(self, samples: List[Tuple[float, float]]):
        # only use samples between 1 and 30 minutes.
        self._x = [1/x[0] for x in samples if x[0] >= 60 and x[1] <= 1800]
        self._y = [x[1] for x in samples if x[0] >= 60 and x[1] <= 1800]
        self._B, self._a = CriticalPower._ols(self._x, self._y)

    @staticmethod
    def _ols(x, y):
        if len(x) != len(y):
            raise ValueError("x and y should have the same dimension")
        if len(x) < 2:
            raise ValueError(
                "At least 2 points are required to estimate the line")

        def demean(x):
            x_ = sum(x) / len(x)
            dx = [xi - x_ for xi in x]
            return dx, x_

        nx, x_ = demean(x)
        ny, y_ = demean(y)

        def cov(x, y):
            return reduce(lambda a, b: a + b,
                          [a*b for a,b in zip(x, y)], 0)

        B = cov(nx, ny)/cov(nx, nx)
        a = y_ - x_*B
        return B, a

    def estimated_power(self, seconds: float):
        """
        Estimates power output possible for a given number of seconds.
        """
        return self._B / seconds + self._a
    
    def estimated_ftp(self):
        return self.estimated_power(1200) * 0.95
