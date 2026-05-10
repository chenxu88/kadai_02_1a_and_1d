from DPS310 import DPS310
from RPR0521rs import RPR0521rs
from SCD41 import SCD41
from BH1750 import BH1750
import time

dps310 = DPS310()
rpr0521rs = RPR0521rs()
scd41 = SCD41()
bh1750 = BH1750()

def initialize():
    dps310.initialize()
    rpr0521rs.initialize()
    scd41.initialize()
    bh1750.initialize()


initialize()
start = time.time()

while True:
    dps310_temp, dps310_pressure = dps310.measure_once()
    rpr0521rs_lux = rpr0521rs.measure_once()
    scd41_co2, scd41_temp, scd41_rh = scd41.measure_once()
    bh1750_lux = bh1750.measure_once()
    
    end = time.time()
    elapsed_time = end - start

    print(f"[TIME: {elapsed_time}s]")
    print("DPS310: Temperature = {:.1f} C, Pressure = {:.2f} hPa".format(dps310_temp, dps310_pressure))
    print("RPR0521rs: Lux = {:.2f} lx".format(rpr0521rs_lux))
    print("SCD41: CO2: {} ppm, Temperature: {:.2f} C, Relative Humidity: {:.2f} %".format(scd41_co2, scd41_temp, scd41_rh))
    print("BH1750: Lux = {:.2f} lx".format(bh1750_lux))
    
    time.sleep(15)