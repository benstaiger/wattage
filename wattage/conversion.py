"""
Defining common unit conversions to avoid litering the code with constants.
"""

def mph_to_kph(mph):
   return mph * 1.60934


def kph_to_mph(kph):
    return kph / 1.60934


# These are essentially useless, but moreso provide
# in-code documentation of units / conversions
def ph_to_ps(ph):
    return ph / 60.0 / 60.0


def km_to_m(km):
    return km * 1000.0


def m_to_km(km):
    return km / 1000.0


def mm_to_m(mm):
    return mm / 1000.0


def m_to_mm(mm):
    return mm * 1000.0
