from machine import Pin, I2C
import time

RPR0521_rs_ADDR = 0x38
RPR0521_rs_SDA_PIN = 5
RPR0521_rs_SCL_PIN = 6
RPR0521_rs_FREQ = 100000
RPR0521_rs_MODE_CONTROL = 0x41
RPR0521_ALS_PS_CONTROL = 0x42
RPR0521_ALS_DATA0_lsb = 0x46
RPR0521_ALS_DATA1_lsb = 0x48

i2c = I2C(0, scl=Pin(RPR0521_rs_SCL_PIN), sda=Pin(RPR0521_rs_SDA_PIN), freq=RPR0521_rs_FREQ)
print("I2C scan:", [hex(addr) for addr in i2c.scan()])

def write_reg(reg, val):
    i2c.writeto_mem(RPR0521_rs_ADDR, reg, bytes([val]))

def read_reg(reg, n):
    return i2c.readfrom_mem(RPR0521_rs_ADDR, reg, n)

def initialize():
    write_reg(RPR0521_rs_MODE_CONTROL, 0x85)
    write_reg(RPR0521_ALS_PS_CONTROL, 0x00)
    time.sleep(1)
    # print("MODE_CONTROL: ", read_reg(RPR0521_rs_MODE_CONTROL, 1))
    # print("ALS_PS_CONTROL: ", read_reg(RPR0521_ALS_PS_CONTROL, 1))

def read_als():
    data0_raw = read_reg(RPR0521_ALS_DATA0_lsb, 2)
    data1_raw = read_reg(RPR0521_ALS_DATA1_lsb, 2)
    # print("data0_raw = ", data0_raw, "data1_raw = ", data1_raw)

    data0 = int.from_bytes(data0_raw, "little")
    data1 = int.from_bytes(data1_raw, "little")
    # print("data0 = ", data0, "data1 = ", data1)
    return data0, data1

def convert_to_lux(data0, data1):
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


initialize()
start = time.time()

while True:
    data0, data1 = read_als()
    # print("raw ALS data: data0 = {}, data1 = {}".format(data0, data1))
    lux = convert_to_lux(data0, data1)
    end = time.time()
    print("[{}s]  RPR-0521rs: Lux = {:.2f} lx".format(end - start, lux))
    time.sleep(15)
