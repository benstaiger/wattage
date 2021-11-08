import math
from typing import NewType


def solve_for_watts(target_velocity,
                        acceleration,
                        slope,
                        total_mass,
                        relative_wind,  # positive is tailwind
                        c_rolling,
                        cda,
                        air_density):
    gravity = 9.81 # m/s**2
    rr_wattage = c_rolling * total_mass * gravity * target_velocity
    pe_wattage = slope * total_mass * gravity * target_velocity
    ke_wattage = total_mass * acceleration * target_velocity
    air_speed = (target_velocity - relative_wind)
    aero_wattage = 0.5 * cda * air_density * air_speed**2 * target_velocity
    total = rr_wattage + pe_wattage + ke_wattage + aero_wattage
    return total


def _newton_method(f, fdx, initial=0, iterations=10):
    def _newton_step(x):
        y = f(x)
        slope = fdx(x)
        intercept = x - y / slope
        error = f(intercept)
        return intercept, error
    
    x, err = _newton_step(initial)
    print(x, err)
    for _ in range(iterations):
        x, err = _newton_step(x)
        print(x, err)
    return x


def solve_for_speed(target_watts,
                    acceleration,
                    slope,
                    total_mass,
#                     relative_wind,  # positive is tailwind
                    c_rolling,
                    cda,
                    air_density):
    def _watts(v):
        return solve_for_watts(
            v,
            acceleration,
            slope,
            total_mass,
            0,  # air_speed
            c_rolling,
            cda,
            air_density
        ) - target_watts

    def _dWdv(v):
        gravity = 9.81  # m/s**2
        return (c_rolling * total_mass * gravity +
                slope * total_mass * gravity +
                total_mass * acceleration +
                0.5 * cda * air_density * 3 * v**2)

    # Use newton method to solve for speed
    return _newton_method(_watts, _dWdv, initial=3, iterations=20)
