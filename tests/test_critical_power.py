import pytest

from wattage.critical_power import CriticalPower


def test_ols():
    x = list(range(10))
    test_B = 2
    test_a = 3
    y = [test_B*xi + test_a for xi in x]
    B, a = CriticalPower._ols(x, y)
    assert B == test_B
    assert a == test_a


def test_estimated_power():
    x = list(range(60, 70))
    test_B = 2
    test_a = 3
    y = [test_B/xi + test_a for xi in x]
    cp = CriticalPower(list(zip([xi for xi in x], y)))
    for xi, yi in zip(x, y):
        assert pytest.approx(yi, rel=0.001) == cp.estimated_power(xi)

def test_estimated_ftp():
    x = list(range(60, 70))
    test_B = 2
    test_a = 3
    y = [test_B/xi + test_a for xi in x]
    cp = CriticalPower(list(zip([xi for xi in x], y)))
    power_20min = test_B/1200 + test_a
    assert pytest.approx(cp.estimated_ftp(), rel=0.001) == power_20min * 0.95
