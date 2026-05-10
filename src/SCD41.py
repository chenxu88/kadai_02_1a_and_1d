from machine import Pin, I2C
import time

SCD41_ADDR = 0x62
SCD41_SDA_PIN = 3 
SCD41_SCL_PIN = 4
SCD41_FREQ = 100000
CMD_START_MEAS= b"\x21\xb1"
CMD_STOP_MEAS= b"\x3f\x86"
CMD_GET_DATA_READY_STATUS = b"\xe4\xb8"
CMD_READ_DATA = b"\xec\x05"

i2c = I2C(0, scl=Pin(SCD41_SCL_PIN), sda=Pin(SCD41_SDA_PIN), freq=SCD41_FREQ)
print("I2C scan:", [hex(addr) for addr in i2c.scan()])

def send_command(cmd):
    i2c.writeto(SCD41_ADDR, cmd)

def start_meas():
    send_command(CMD_START_MEAS)
    print("SCD41 started")
    time.sleep(5)

def stop_meas():
    send_command(CMD_STOP_MEAS)
    print("SCD41 stoped")
    time.sleep(1)

def ready_status():
    send_command(CMD_GET_DATA_READY_STATUS)
    data = i2c.readfrom(SCD41_ADDR,3)
    raw = (data[0] << 8) | data[1]
    ready = (raw & 0x07FF) != 0
    # print("Data status: ", ready)
    return ready

def read_data():
    send_command(CMD_READ_DATA)
    time.sleep_ms(50)
    measurement = i2c.readfrom(SCD41_ADDR, 9)
    # print(measurement)
    return measurement

def data_convert(data):
    co2_raw = (data[0] << 8) | data[1]
    temp_raw = (data[3] << 8) | data[4]
    rh_raw = (data[6] << 8) | data[7]
    
    co2 = co2_raw
    temp = -45 + 175 * (temp_raw / 65536)
    rh = 100 * (rh_raw / 65536)

    return co2, temp, rh

def measure_once():
    # stop_meas()
    # start_meas()
    if ready_status():
        raw = read_data()
        co2, temp, rh = data_convert(raw)
        end = time.time()
        print("[{}s]  CO2: {} ppm, Temperature: {:.2f} C, Relative Humidity: {:.2f} %".format(end - start, co2, temp, rh))

# Initialize
print("Measure Started")
stop_meas()
start_meas()
start = time.time()

while True:
    if ready_status():
        measure_once()

    else:
        print("Data not ready")

    time.sleep(15)

