from wattage import gearing


def test_find_cassette():
    chainring = 53
    ratio = chainring / 11.0
    setups = gearing.find_cassette(chainring, ratio, rel_err=1e-4)
    assert len(setups) == 1 
    assert setups[0]["cassette"] == 11

    setups = gearing.find_cassette(chainring, ratio, rel_err=0.1)
    assert len(setups) == 1 
    assert setups[0]["cassette"] == 11


def test_find_setups():
    chainring = 53
    ratio = chainring / 11.0
    setups = gearing.find_setups(ratio, rel_err=1e-4)
    found_real_setup = False
    print(setups)
    for s in setups:
        if s["cassette"] == 11 and s["chainring"] == 53:
            found_real_setup = True
    assert found_real_setup
