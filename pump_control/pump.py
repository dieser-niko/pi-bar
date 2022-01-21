import gpiozero

class Pump:
    def __init__(self, pin: int, speed: int or float):
        self.pin = pin
        self.speed = speed
        self.pump = gpiozero.OutputDevice(pin, active_high=True, initial_value=False)

    def on(self):
        self.pump.on()

    def off(self):
        self.pump.off()

    def state(self):
        return bool(self.pump.value)