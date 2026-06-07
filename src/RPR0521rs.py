from machine import Pin, I2C
import time

from config import RPR0521RS_CONFIG


class RPR0521rs:
    I2C_ID = RPR0521RS_CONFIG["i2c_id"]
    ADDR = RPR0521RS_CONFIG["addr"]
    SDA_PIN = RPR0521RS_CONFIG["sda_pin"]
    SCL_PIN = RPR0521RS_CONFIG["scl_pin"]
    FREQ = RPR0521RS_CONFIG["freq"]

    MODE_CONTROL = 0x41
    ALS_PS_CONTROL = 0x42
    ALS_DATA0_LSB = 0x46
    ALS_DATA1_LSB = 0x48

    def __init__(self):
        self.i2c = I2C(self.I2C_ID, scl=Pin(self.SCL_PIN), sda=Pin(self.SDA_PIN), freq=self.FREQ)
        self.initialized = False

    def write_reg(self, reg, val):
        self.i2c.writeto_mem(self.ADDR, reg, bytes([val]))

    def read_reg(self, reg, n):
        return self.i2c.readfrom_mem(self.ADDR, reg, n)

    def initialize(self):
        self.write_reg(self.MODE_CONTROL, 0x85)
        self.write_reg(self.ALS_PS_CONTROL, 0x00)
        time.sleep(1)
        self.initialized = True
        print("RPR0521rs Initialize complete")

    def is_initialized(self):
        return self.initialized

    def read_als(self):
        if not self.initialized:
            self.initialize()

        data0_raw = self.read_reg(self.ALS_DATA0_LSB, 2)
        data1_raw = self.read_reg(self.ALS_DATA1_LSB, 2)

        data0 = int.from_bytes(data0_raw, "little")
        data1 = int.from_bytes(data1_raw, "little")
        return data0, data1

    def convert_to_lux(self, data0, data1):
        if data0 == 0:
            return 0.0

        ratio = data1 / data0

        if ratio < 0.595:
            lux = 1.682 * data0 - 1.877 * data1
        elif ratio < 1.015:
            lux = 0.644 * data0 - 0.132 * data1
        elif ratio < 1.352:
            lux = 0.756 * data0 - 0.243 * data1
        elif ratio < 3.053:
            lux = 0.766 * data0 - 0.25 * data1
        else:
            lux = 0.0

        if lux < 0:
            lux = 0.0

        return lux

    def measure_once(self):
        data0, data1 = self.read_als()
        lux = self.convert_to_lux(data0, data1)
        return lux, data1
