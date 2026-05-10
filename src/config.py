COMMON_I2C_FREQ = 100000


DPS310_CONFIG = {
    "i2c_id": 0,
    "sda_pin": 3,
    "scl_pin": 4,
    "freq": COMMON_I2C_FREQ,
    "addr": 0x77,
}

SCD41_CONFIG = {
    "i2c_id": 0,
    "sda_pin": 3,
    "scl_pin": 4,
    "freq": COMMON_I2C_FREQ,
    "addr": 0x62,
}

RPR0521RS_CONFIG = {
    "i2c_id": 0,
    "sda_pin": 3,
    "scl_pin": 4,
    "freq": COMMON_I2C_FREQ,
    "addr": 0x38,
}

BH1750_CONFIG = {
    "i2c_id": 0,
    "sda_pin": 3,
    "scl_pin": 4,
    "freq": COMMON_I2C_FREQ,
    "addr": 0x23,
}
