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


def test_newton_method_linear():
    slope = 3
    y_int = 2
    x_int = -y_int / slope
    def f(x):
        return slope * x + y_int
    def dfdx(x):
        return slope
    estimated_x_int = wattage._newton_method(f, dfdx)
    assert pytest.approx(estimated_x_int, rel=1e-4) == x_int


def test_newton_method_quadratic():
    def f2(x):
        return (x-2)**2
    def df2dx(x):
        # (x-2)**2 = x**2 - 4x + 4
        return 2*x - 4
    estimated_x_int2 = wattage._newton_method(f2, df2dx, iterations=20)
    assert pytest.approx(estimated_x_int2, rel=1e-4) == 2


def test_velocity_simple():
    air_density = 1.226  # kg/m**3, average @ sea-level
    rider_mass = 75  # kg
    bike_mass = 8  # kg
    crr = 0.004
    cda = 0.25
    gradient = 0
    wind_speed = 0  # m/s
    expected_watts = 246.395
    target_speed = 40 * 1000.0 / 60.0 / 60.0  # 40kph in m/s
    watts = wattage.solve_for_watts(
        target_velocity=target_speed,
        acceleration=0,
        slope=gradient,
        total_mass=rider_mass+bike_mass,
        relative_wind=wind_speed,
        c_rolling=crr,
        cda=cda,
        air_density=air_density
    )
    estimated_speed = wattage.solve_for_speed(
        watts,
        acceleration=0,
        slope=gradient,
        total_mass=rider_mass+bike_mass,
        c_rolling=crr,
        cda=cda,
        air_density=air_density
    )
    # assert estimated_speed == target_speed
