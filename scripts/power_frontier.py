import matplotlib.pyplot as plt
import wattage

from wattage.conversion import mph_to_kph, kph_to_mph, km_to_m, ph_to_ps
from wattage.wattage import solve_for_speed, solve_for_watts

# Estimate CdA from recent race data using an assumed Crr.
# Plot an estimated power to speed curve. Maybe give it a confidence band?
if __name__ == "__main__":
    # We will just do a linear search on solve_for_watts untile we find
    # and appropriate CdA.
    watts = 225
    speed = ph_to_ps(km_to_m(mph_to_kph(22)))  # 22 mph in m/s #9.83488
    mass = 82 + 9  # self + bike + equipment
    cdas = [0.22 + 0.01*i for i in range(20)]
    air_density = 1.18  # https://www.omnicalculator.com/physics/air-density#:~:text=Our%20air%20density%20calculator%20uses,%2F%20(243.12%20%2B%20T)%20.
    rolling = 0.004
    required = [solve_for_watts(target_velocity=speed, acceleration=0, slope=0, total_mass=mass, relative_wind=0, c_rolling=0.004, cda=cda, air_density=air_density) for cda in cdas]
    print(list(zip(cdas, required)))

    # cda ~.34 assuming these conditions...which is very high compared to
    # claimed cdas of timetrialists. Like 0.2-0.25 is usually a range
    # for people on tt bikes with something like 0.4 being a larger cyclist
    # on a road bike.
    lower = 0.3 # more optimistic, but stil like 20% savings possible...
    for cda in [0.3, 0.34]:
        wattages = range(185, 400, 5)
        speeds = [
            solve_for_speed(
                watts,
                acceleration=0,
                slope=0,
                total_mass=mass,
                c_rolling=rolling,
                cda=cda,
                air_density=air_density
            )
            for watts in wattages
        ]
        speeds = [kph_to_mph(s / 1000 * 60 * 60) for s in speeds]
        hour_40km = 11.1111
        w = solve_for_watts(target_velocity=hour_40km, acceleration=0, slope=0, total_mass=mass, relative_wind=0, c_rolling=0.004, cda=cda, air_density=air_density)
        plt.plot(wattages, speeds)
        plt.scatter([w], [kph_to_mph(40)])
    plt.show()
