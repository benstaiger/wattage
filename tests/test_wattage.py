import pytest

from wattage import wattage


def test_wattage_simple():
    air_density = 1.226  # kg/m**3, average @ sea-level
    rider_mass = 75  # kg
    bike_mass = 8  # kg
    crr = 0.004
    cda = 0.25
    gradient = 0
    wind_speed = 0  # m/s
    expected_watts = 246.395
    speed = 40 * 1000.0 / 60.0 / 60.0  # 40kph in m/s
    watts = wattage.solve_for_watts(
        target_velocity=speed,
        acceleration=0,
        slope=gradient,
        total_mass=rider_mass+bike_mass,
        relative_wind=wind_speed,
        c_rolling=crr,
        cda=cda,
        air_density=air_density
    )
    assert pytest.approx(watts, rel=0.01) == expected_watts
    