import matplotlib.pyplot as plt

from wattage.wheel import Wheel
from wattage.critical_power import CriticalPower
from wattage.gearing import find_gear_ratio, find_setups


def plot_power_curve(power_curve: CriticalPower, samples=None):
    minutes =list(range(30,1800+60,30)) 
    plt.plot(minutes, [power_curve.estimated_power(m) for m in minutes])
    ftp = power_curve.estimated_ftp()
    plt.axhline(ftp, color="r")
    plt.title(f"Critical Power Curve (FTP: {int(ftp)})")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Watts")

    if samples:
        plt.scatter([x[0] for x in samples],
                    [x[1] for x in samples])
    plt.show()


def plot_setups(setups):
    chainrings = [x[0] for x in setups]
    cogs = [x[1] for x in setups]
    plt.scatter(chainrings, cogs)
    plt.xlabel("Chainring Teeth")
    plt.ylabel("Cog Teeth")
    plt.show()


def min_gearing_requied_at_ftp(power_curve, cadence, incline, wheel, total_mass, chainrings):
    ratio = find_gear_ratio(power_curve.estimated_ftp(), cadence, incline, wheel, total_mass)
    print(f"estimated gear ratio: {ratio}")

    options = []
    for c in chainrings:
        setups = find_setups(ratio, [c], rel_err=0.04)

        # Find the best ratio that would be "possible"
        if setups:
            setups = sorted(setups, key=lambda x: x["gear_ratio"])
            # bisect_left doesn't have a "key" argument
            # until python 3.10
            def lower_bound(x):
                bound = None
                for xi in x:
                    if xi["gear_ratio"] < ratio:
                        bound = xi
                    else:
                        break
                return bound
            best = lower_bound(setups)
            if best:
                options.append((best["chainring"],
                                best["cassette"]))
    return options


def main():
    power_pr = [
        (60, 450),
        (300, 280),
        (600, 250),
    ]
    power_curve = CriticalPower(power_pr)
    plot_power_curve(power_curve, power_pr)

    wheels = Wheel("700c/29er", "25mm")
    incline = 0.124  # estimated up 17th street based on Strava segments
    chainrings = [34, 37, 48, 53]
    total_mass = 90  # rider + bike
    desired_cadence = 80
    options = min_gearing_requied_at_ftp(power_curve, desired_cadence, incline, wheels, total_mass, chainrings)
    print("Possibilities (Chainring, cassette)")
    print(options)


if __name__ == "__main__":
    main()
