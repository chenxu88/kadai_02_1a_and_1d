from machine import Pin, I2C
import time

from config import DPS310_CONFIG


class DPS310:
    I2C_ID = DPS310_CONFIG["i2c_id"]
    SDA_PIN = DPS310_CONFIG["sda_pin"]
    SCL_PIN = DPS310_CONFIG["scl_pin"]
    FREQ = DPS310_CONFIG["freq"]

    ADDR = DPS310_CONFIG["addr"]
    REG_ID = 0x0D
    CHIP_ID = 0x10

    REG_PRS_B2 = 0x00
    REG_PRS_CFG = 0x06
    REG_TMP_B2 = 0x03
    REG_TMP_CFG = 0x07
    REG_MEAS_CFG = 0x08
    REG_COEF = 0x10

    TMP_CFG = 0x80
    SCALE_FACTOR = 524288.0

    def __init__(self):
        self.i2c = I2C(self.I2C_ID, scl=Pin(self.SCL_PIN), sda=Pin(self.SDA_PIN), freq=self.FREQ)
        self.coeffs = None

    def write_reg(self, reg, value):
        self.i2c.writeto_mem(self.ADDR, reg, bytes([value]))

    def read_reg(self, reg, n):
        return self.i2c.readfrom_mem(self.ADDR, reg, n)

    def check_chip_id(self):
        chip_id = self.read_reg(self.REG_ID, 1)[0]
        if chip_id == self.CHIP_ID:
            return True
        return False

    def sign_extend(self, value, bits):
        sign_bit = 1 << (bits - 1)
        return (value ^ sign_bit) - sign_bit

    def initialize(self):
        if not self.check_chip_id():
            raise RuntimeError("DPS310 chip ID error")

        self.coeffs = self.read_coeffs()
        print("DPS310 Initialize complete")

    def read_coeffs(self):
        buf = self.read_reg(self.REG_COEF, 18)

        c0 = (buf[0] << 4) | ((buf[1] >> 4) & 0x0F)
        c1 = ((buf[1] & 0x0F) << 8) | buf[2]

        c00 = (buf[3] << 12) | (buf[4] << 4) | ((buf[5] >> 4) & 0x0F)
        c10 = ((buf[5] & 0x0F) << 16) | (buf[6] << 8) | buf[7]

        c01 = (buf[8] << 8) | buf[9]
        c11 = (buf[10] << 8) | buf[11]
        c20 = (buf[12] << 8) | buf[13]
        c21 = (buf[14] << 8) | buf[15]
        c30 = (buf[16] << 8) | buf[17]

        coeffs = {
            "c0": self.sign_extend(c0, 12),
            "c1": self.sign_extend(c1, 12),
            "c00": self.sign_extend(c00, 20),
            "c10": self.sign_extend(c10, 20),
            "c01": self.sign_extend(c01, 16),
            "c11": self.sign_extend(c11, 16),
            "c20": self.sign_extend(c20, 16),
            "c21": self.sign_extend(c21, 16),
            "c30": self.sign_extend(c30, 16),
        }
        return coeffs

    def ready_status(self, mask):
        meas_cfg = self.read_reg(self.REG_MEAS_CFG, 1)[0]
        ready = (meas_cfg & mask) != 0
        return ready



    def start_temp_measurement(self):
        self.write_reg(self.REG_TMP_CFG, self.TMP_CFG)
        self.write_reg(self.REG_MEAS_CFG, 0x02)

    def read_temp_raw(self):
        data_raw = self.read_reg(self.REG_TMP_B2, 3)
        data = (data_raw[0] << 16) | (data_raw[1] << 8) | data_raw[2]
        return self.sign_extend(data, 24)

    def convert_temp(self, raw_temp):
        traw_sc = raw_temp / self.SCALE_FACTOR
        temp = self.coeffs["c0"] * 0.5 + self.coeffs["c1"] * traw_sc
        return temp



    def start_pressure_measurement(self):
        self.write_reg(self.REG_PRS_CFG, 0x00)
        self.write_reg(self.REG_MEAS_CFG, 0x01)

    def read_pressure_raw(self):
        data_raw = self.read_reg(self.REG_PRS_B2, 3)
        data = (data_raw[0] << 16) | (data_raw[1] << 8) | data_raw[2]
        return self.sign_extend(data, 24)

    def convert_pressure(self, raw_pressure, raw_temp):
        traw_sc = raw_temp / self.SCALE_FACTOR
        praw_sc = raw_pressure / self.SCALE_FACTOR

        pressure = (
            self.coeffs["c00"]
            + praw_sc
            * (
                self.coeffs["c10"]
                + praw_sc * (self.coeffs["c20"] + praw_sc * self.coeffs["c30"])
            )
            + traw_sc * self.coeffs["c01"]
            + traw_sc
            * praw_sc
            * (self.coeffs["c11"] + praw_sc * self.coeffs["c21"])
        )
        return pressure / 100.0



    def measure_once(self):
        if self.coeffs is None:
            self.initialize()

        self.start_temp_measurement()
        time.sleep_ms(10)
        if not self.ready_status(0x20):
            raise RuntimeError("Temperature data not ready")

        raw_temp = self.read_temp_raw()

        self.start_pressure_measurement()
        time.sleep_ms(10)
        if not self.ready_status(0x10):
            raise RuntimeError("Pressure data not ready")

        raw_pressure = self.read_pressure_raw()

        temp = self.convert_temp(raw_temp)
        pressure = self.convert_pressure(raw_pressure, raw_temp)

        return temp, pressure
