import time
import threading


class Pump:
    def __init__(self, pin: int, speed: int or float):
        self.pin = pin
        self.speed = speed
        self._value = 0

    def _start(self):
        while self._value:
            print(self.pin, 1)
            time.sleep(self.speed)

    def on(self):
        self.value = 1

    def off(self):
        self.value = 0

    def state(self):
        return bool(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        old_value = self._value
        self._value = value
        if not old_value and value:
            threading.Thread(target=self._start, daemon=True).start()
