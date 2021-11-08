import math
import numpy as np
import pandas as pd
import pytest

from wattage import wheel


def test_wheel_data():
    """Test wheel constructor vs underlying data."""
    data = pd.read_csv("data/wheel.csv", 
        dtype={"rim": str, "tire": str, "rim_mm": np.float32, "tire_mm": np.float32, "diameter_mm": np.float32, "circumference_mm": np.float32})

    for _, row in data.iterrows():
        wheel0 = wheel.Wheel(row.rim, row.tire)

        # Test interface
        assert wheel0.diameter > 0
        assert wheel0.radius > 0
        assert wheel0.radius == wheel0.diameter / 2.0
        assert wheel0.cirumference > 0

        # Test data loading
        assert wheel0.rim == row.rim
        assert wheel0.tire == row.tire
        assert wheel0.diameter == row.diameter_mm
        assert wheel0.cirumference == row.circumference_mm

        # Test data validity
        assert pytest.approx(row.diameter_mm, 0.1) == (row.rim_mm + 2*row.tire_mm)
        assert pytest.approx(row.circumference_mm, 0.1) == (row.diameter_mm * math.pi)


def test_invalid_construction():
    try:
        wheel0 = wheel.Wheel("700c/29er", "Unknown")
        assert False
    except ValueError:
        pass


def test_cadence():
    wheel0 = wheel.Wheel("700c/29er", "25mm")
    speed = 40.0 * 1000.0 / 60.0 / 60.0  # 40kph
    # 11.111m/s with wheel circumference of 2.11115m
    # -> ~5.263 rps
    # -> ~315.783 rpm
    assert pytest.approx(wheel0.cadence(speed), rel=0.01) == 315.783
    # 53-11 gear-ratio
    ratio = 53.0/11.0
    assert pytest.approx(wheel0.cadence(speed, ratio), rel=0.01) == 315.783 / ratio


def test_gear_ratio():
    wheel0 = wheel.Wheel("700c/29er", "25mm")
    speed = 54.9 * 1000.0 / 60.0 / 60.0  # 40kph in m/s
    ratio = 53.0/11.0
    cadence = 90.0
    assert pytest.approx(wheel0.gear_ratio(speed, cadence), rel=0.01) == ratio


def test_speed():
    wheel0 = wheel.Wheel("700c/29er", "25mm")
    speed = 54.9 * 1000.0 / 60.0 / 60.0  # 40kph in m/s
    ratio = 53.0/11.0
    cadence = 90.0
    assert pytest.approx(wheel0.speed(cadence, ratio), rel=0.01) == speed
