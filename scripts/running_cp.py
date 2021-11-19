import matplotlib.pyplot as plt

from wattage.critical_power import CriticalPower
from wattage import conversion as cvt

def main():
    pbs = [
        # [meters, seconds]
        [1000, 4*60 + 30],  # 1K
        [1609, 7*60 + 31],  # 1mile
        [5000, 26*60 + 42],   # 5K this is probably an underestimate
    ]
    ms = [
        [s, m / s] for m, s in pbs
    ]

    critical_speed = CriticalPower(ms)

    times = list(range(4*60, 60*60 + 1, 60))
    speed = [critical_speed.estimated_power(t) for t in times]

    plt.plot(times, speed, label="CS Curve")
    plt.scatter([t for t, _ in ms], [s for _, s in ms], label="Samples")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Speed (m/s)")
    plt.axhline(critical_speed._a, color="r", label="CS")
    mph_cs = (critical_speed._a  * 2.23694)
    pace_cs = 1 / mph_cs * 60.0
    print(mph_cs, pace_cs)
    plt.title(f"Critical Running Speed (Critical Pace: {pace_cs :.2f}min/mile)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
