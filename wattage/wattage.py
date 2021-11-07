import math


def wattage_requirement(target_velocity,
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
    # print(f"RR:{rr_wattage:0.1f} PE:{pe_wattage:0.1f} KE:{ke_wattage:0.1f} AE:{aero_wattage:0.1f} TOT:{total:0.1f}")
    return total


def wattage_steady_state(target_velocity,
                         total_mass,
                         c_rolling,
                         cda,
                         air_density):
    return wattage_requirement(target_velocity, 0, 0, total_mass, 0, c_rolling, cda, air_density)
