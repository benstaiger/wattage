import matplotlib.pyplot as plt

from wattage.wheel import Wheel
from wattage.critical_power import CriticalPower
from wattage.gearing import find_cassette, find_gear_ratio, find_setups


def plot_power_curve(ax, power_curve: CriticalPower, samples=None):
    minutes =list(range(30,1800+60,30)) 
    ax.plot(minutes, [power_curve.estimated_power(m) for m in minutes])
    ftp = power_curve.estimated_ftp()
    ax.axhline(ftp, color="r")
    ax.set_title(f"Critical Power Curve (FTP: {int(ftp)})")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Watts")

    if samples:
        ax.scatter([x[0] for x in samples],
                    [x[1] for x in samples])


def plot_setups(ax, setups, ratio):
    chainrings = [x[0] for x in setups]
    cogs = [x[1] for x in setups]
    ax.scatter(chainrings, cogs)
    ax.set_title(f"Setup Options (Gear Ratio: {ratio: .2f})")
    ax.set_xlabel("Chainring Teeth")
    ax.set_ylabel("Cog Teeth")
    ax.plot([0, ratio*100], [0, 100], color="r")
    for r, c in zip(chainrings, cogs):
        print(f"{r}-{c}", (r,  c))
        ax.annotate(f"{r}-{c}", (r,  c))


def min_gearing_requied_at_ftp(power_curve, cadence, incline, wheel, total_mass, chainrings):
    ratio = find_gear_ratio(power_curve.estimated_ftp(), cadence, incline, wheel, total_mass)

    options = []
    for c in chainrings:
        setups = find_cassette(c, ratio, rel_err=0.04)

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
    return ratio, options


def plot_parameters(ax, incline, chainrings, total_mass, desired_cadence):
    ax.table(
        cellText=[[f"{incline*100}%"],
                   [f"{','.join([str(c) for c in chainrings])}"],
                   [f"{total_mass} kg"],
                   [f"{desired_cadence} rpm"]],
        rowLabels=[
            "incline",
            "chainrings",
            "total mass",
            "desired cadence"]
    )


def main():
    power_pr = [
        (60, 450),
        (300, 280),
        (600, 250),
    ]
    power_curve = CriticalPower(power_pr)

    wheels = Wheel("700c/29er", "25mm")
    incline = 0.124  # estimated up 17th street based on Strava segments
    chainrings = [34, 37, 48, 53]
    total_mass = 90  # rider + bike
    desired_cadence = 80
    ratio, options = min_gearing_requied_at_ftp(power_curve, desired_cadence, incline, wheels, total_mass, chainrings)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    plot_power_curve(ax1, power_curve, power_pr)
    plot_setups(ax2, options, ratio)
    fig.suptitle(f"Incline={incline*100}%, Total Mass={total_mass}kg, Cadence={desired_cadence}rpm, Possible Chainrings={chainrings}")
    plt.show()


if __name__ == "__main__":
    main()
