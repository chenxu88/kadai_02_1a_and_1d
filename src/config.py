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

WIFI_CONFIGS = [
    {
        "ssid": "JAISTALL",
        "password": "",
    }
]

MQTT_CONFIGS = [
    {
        "host": "150.65.230.59",
        "port": "1883",
        "client_id": "mqtt_esp32",
    }
]

try:
    from config_local import WIFI_CONFIGS as LOCAL_WIFI_CONFIGS
    WIFI_CONFIGS = LOCAL_WIFI_CONFIGS + WIFI_CONFIGS
except ImportError:
    pass

try:
    from config_local import MQTT_CONFIGS as LOCAL_MQTT_CONFIGS
    MQTT_CONFIGS = LOCAL_MQTT_CONFIGS + MQTT_CONFIGS
except ImportError:
    pass

