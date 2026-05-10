from machine import Pin, I2C
import time

BH1750_ADDR = 0x23
BH1750_SDA_PIN = 7
BH1750_SCL_PIN = 8
BH1750_FREQ = 100000

CMD_POWER_ON = b'\x01'
COM_RESET = b'\07'
COM_HIGH_RES_MODE2 = b'\x11'

i2c = I2C(0, scl=Pin(BH1750_SCL_PIN), sda=Pin(BH1750_SDA_PIN), freq=BH1750_FREQ)
# print("I2C scan:", [hex(addr) for addr in i2c.scan()])

def send_command(cmd):
    i2c.writeto(BH1750_ADDR, cmd)

def initialize():
    send_command(CMD_POWER_ON)
    time.sleep(1)
    send_command(COM_RESET)
    time.sleep(1)
    send_command(COM_HIGH_RES_MODE2)
    time.sleep(1)
    print("BH1750 Initialize complete")

def read_data():
    data_raw = i2c.readfrom(BH1750_ADDR, 2)
    # print("Raw data = ", data_raw)
    data = (data_raw[0] << 8) | data_raw[1]
    # print("Data = ", data)
    return data

def convert_to_lux(data):
    lux = data / 1.2
    return lux

initialize()
start = time.time()

while True:
    data = read_data()
    lux = convert_to_lux(data)
    end = time.time()
    print("[{}s]  BH1750: Lux = {:.2f} lx".format(end - start, lux))
    time.sleep(15)
