from machine import Pin, Timer
import neopixel

class LED:
    def __init__(self):
        self.np = neopixel.NeoPixel(Pin(2, Pin.OUT), 1)
        self.timer = Timer(0)
        self.is_on = False

    def _toggle(self, timer):
        if self.is_on:
            self.np[0] = (0, 0, 0)
            self.is_on = False
        else:
            self.np[0] = (20, 0, 0)
            self.is_on = True
        self.np.write()

    def start_blink(self, period=300):
        self.timer.deinit()
        self.is_on = False
        self.timer.init(period=period, mode=Timer.PERIODIC, callback=self._toggle)

    def off(self):
        self.timer.deinit()
        self.np[0] = (0, 0, 0)
        self.np.write()
        self.is_on = False