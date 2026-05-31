from machine import Pin
import neopixel

class LED:
    def __init__(self):
        self.np = neopixel.NeoPixel(Pin(2, Pin.OUT), 1)

    def on(self):
        self.np[0] = (20, 0, 0)
        self.np.write()

    def off(self):
        self.np[0] = (0, 0, 0)
        self.np.write()
