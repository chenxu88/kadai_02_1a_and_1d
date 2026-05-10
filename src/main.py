from DPS310 import DPS310

dps310 = DPS310()
dps310_temp, dps310_pressure = dps310.measure_once()
print("DPS310: Temperature = {:.1f} C, Pressure = {:.2f} hPa".format(temp, pressure))