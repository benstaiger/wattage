from wattage.wattage import solve_for_speed
from wattage.wheel import Wheel


_chainrings = list(range(30,63,1))
_cassettes = list(range(10,51,1))


# Maybe this should be client code. That way gearing
# doesn't need to know anything about the modeling...
def find_gear_ratio(watts: float, cadence: float, incline: float, wheel: Wheel, total_mass, crr=0.004, cda=0.3, air_density=1.226):
    expected_speed = solve_for_speed(
        watts,
        0,  # acceleration
        incline,
        total_mass,
        crr,
        cda,
        air_density
    )
    return wheel.gear_ratio(speed=expected_speed, cadence=cadence)


def find_cassette(chainring, gear_ratio, rel_err=0.05):
    setups = []
    for c in _cassettes:
        if abs(gear_ratio - chainring / c) < rel_err:
            setups.append({
                "chainring": chainring,
                "cassette": c,
                "gear_ratio": chainring / c,
                "rel_err": abs(gear_ratio - chainring / c),
            })
    return setups


def find_setups(gear_ratio, rel_err=0.05):
    """
    return a list of chainring / cassettes that will contain the 
    desired ratio.
    """
    setups = []
    for r in _chainrings:
        setups.extend(find_cassette(r, gear_ratio, rel_err))
    return setups