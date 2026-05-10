from DPS310 import DPS310
from RPR0521rs import RPR0521rs
from SCD41 import SCD41

dps310 = DPS310()
dps310.initialize()
rpr0521rs = RPR0521rs()
rpr0521rs.initialize()
scd41 = SCD41()
scd41.initialize()


dps310_temp, dps310_pressure = dps310.measure_once()
print("DPS310: Temperature = {:.1f} C, Pressure = {:.2f} hPa".format(dps310_temp, dps310_pressure))


rpr0521rs_lux = rpr0521rs.measure_once()
print("RPR0521rs: Lux = {:.2f} lx".format(rpr0521rs_lux))

scd41_co2, scd41_temp, scd41_rh = scd41.measure_once()
print("CO2: {} ppm, Temperature: {:.2f} C, Relative Humidity: {:.2f} %".format(scd41_co2, scd41_temp, scd41_rh))

