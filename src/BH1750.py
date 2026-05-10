from machine import Pin, I2C
import time

from config import BH1750_CONFIG


class BH1750:
    I2C_ID = BH1750_CONFIG["i2c_id"]
    ADDR = BH1750_CONFIG["addr"]
    SDA_PIN = BH1750_CONFIG["sda_pin"]
    SCL_PIN = BH1750_CONFIG["scl_pin"]
    FREQ = BH1750_CONFIG["freq"]

    CMD_POWER_ON = b"\x01"
    CMD_RESET = b"\x07"
    CMD_HIGH_RES_MODE = b"\x10"

    def __init__(self):
        self.i2c = I2C(self.I2C_ID, scl=Pin(self.SCL_PIN), sda=Pin(self.SDA_PIN), freq=self.FREQ)
        self.initialized = False

    def send_command(self, cmd):
        self.i2c.writeto(self.ADDR, cmd)

    def initialize(self):
        self.send_command(self.CMD_POWER_ON)
        time.sleep(1)
        self.send_command(self.CMD_RESET)
        time.sleep(1)
        self.send_command(self.CMD_HIGH_RES_MODE)
        time.sleep(1)
        self.initialized = True
        print("BH1750 Initialize complete")

    def is_initialized(self):
        return self.initialized

    def read_data(self):
        if not self.initialized:
            self.initialize()

        data_raw = self.i2c.readfrom(self.ADDR, 2)
        data = (data_raw[0] << 8) | data_raw[1]
        return data

    def convert_to_lux(self, data):
        lux = data / 1.2
        return lux

    def measure_once(self):
        data = self.read_data()
        lux = self.convert_to_lux(data)
        return lux
