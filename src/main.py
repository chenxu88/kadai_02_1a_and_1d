from DPS310 import DPS310
from RPR0521rs import RPR0521rs

dps310 = DPS310()
dps310.initialize()
rpr0521rs = RPR0521rs()
rpr0521rs.initialize()

dps310_temp, dps310_pressure = dps310.measure_once()
print("DPS310: Temperature = {:.1f} C, Pressure = {:.2f} hPa".format(dps310_temp, dps310_pressure))


rpr0521rs_lux = rpr0521rs.measure_once()
print("RPR0521rs: Lux = {:.2f} lx".format(rpr0521rs_lux))