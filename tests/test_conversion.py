import pytest

from wattage import conversion


def test_kph_to_mph():
    assert pytest.approx(conversion.kph_to_mph(5), abs=0.1) == 3.1


def test_mph_to_kph():
    assert pytest.approx(conversion.mph_to_kph(3.1), abs=0.1) == 5


def test_si_conversion():
    assert conversion.m_to_mm(1) == 1000
    assert conversion.mm_to_m(1) == 0.001