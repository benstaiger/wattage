import numpy as np
import pandas as pd

from wattage.conversion import mm_to_m


_data = pd.DataFrame()


def _init():
    global _data
    _data = pd.read_csv("data/wheel.csv", dtype={"rim": str, "tire": str, "rim_mm": np.float32, "tire_mm": np.float32, "diameter_mm": np.float32, "circumference_mm": np.float32})


class Wheel:
    def __init__(self, rim: str, tire: str):
        if _data.empty:
            _init()
        if (rim not in _data.rim.unique()):
            raise ValueError(f"Rim type, {rim}, not found in database.")
        if (tire not in _data.tire.unique()):
            raise ValueError(f"Tire type, {tire}, not found in database.")

        self._rim = rim
        self._tire = tire
        values = _data[(_data.rim == rim) & (_data.tire == tire)]
        if values.empty:
            raise ValueError(f"Rim/Tire pair {rim}, {tire} not found in database.")
        info = values.iloc[0]
        self._diameter = float(info.diameter_mm)
        self._circumference = float(info.circumference_mm)

    @property
    def rim(self):
        return self._rim
    
    @property
    def tire(self):
        return self._tire

    @property
    def diameter(self):
        return self._diameter

    @property
    def radius(self):
        return self.diameter / 2.0
    
    @property
    def cirumference(self):
        return self._circumference
    
    def rpm(self, speed: float, gear_ratio: float=1):
        """Take a speed in m/s and return an rpm"""
        rotations_per_second = speed / mm_to_m(self.cirumference)
        return rotations_per_second * 60 / gear_ratio
