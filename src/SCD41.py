from machine import Pin, I2C
import time

from config import SCD41_CONFIG


class SCD41:
    I2C_ID = SCD41_CONFIG["i2c_id"]
    ADDR = SCD41_CONFIG["addr"]
    SDA_PIN = SCD41_CONFIG["sda_pin"]
    SCL_PIN = SCD41_CONFIG["scl_pin"]
    FREQ = SCD41_CONFIG["freq"]

    CMD_START_MEAS = b"\x21\xb1"
    CMD_STOP_MEAS = b"\x3f\x86"
    CMD_GET_DATA_READY_STATUS = b"\xe4\xb8"
    CMD_READ_DATA = b"\xec\x05"

    def __init__(self):
        self.i2c = I2C(self.I2C_ID, scl=Pin(self.SCL_PIN), sda=Pin(self.SDA_PIN), freq=self.FREQ)
        self.initialized = False

    def send_command(self, cmd):
        self.i2c.writeto(self.ADDR, cmd)

    def start_meas(self):
        self.send_command(self.CMD_START_MEAS)
        # print("SCD41 started")
        time.sleep(5)

    def stop_meas(self):
        self.send_command(self.CMD_STOP_MEAS)
        # print("SCD41 stoped")
        time.sleep(1)

    def initialize(self):
        self.stop_meas()
        self.start_meas()
        self.initialized = True
        print("SCD41 Initialize complete")

    def is_initialized(self):
        return self.initialized

    def ready_status(self):
        self.send_command(self.CMD_GET_DATA_READY_STATUS)
        data = self.i2c.readfrom(self.ADDR, 3)
        raw = (data[0] << 8) | data[1]
        ready = (raw & 0x07FF) != 0
        return ready

    def read_data(self):
        if not self.initialized:
            self.initialize()

        self.send_command(self.CMD_READ_DATA)
        time.sleep_ms(50)
        measurement = self.i2c.readfrom(self.ADDR, 9)
        return measurement

    def data_convert(self, data):
        co2_raw = (data[0] << 8) | data[1]
        temp_raw = (data[3] << 8) | data[4]
        rh_raw = (data[6] << 8) | data[7]

        co2 = co2_raw
        temp = -45 + 175 * (temp_raw / 65536)
        rh = 100 * (rh_raw / 65536)

        return co2, temp, rh

    def measure_once(self):
        if not self.initialized:
            self.initialize()

        if not self.ready_status():
            raise RuntimeError("SCD41 data not ready")

        raw = self.read_data()
        co2, temp, rh = self.data_convert(raw)
        return co2, temp, rh
