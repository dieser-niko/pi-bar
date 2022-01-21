# Please remove all signs of simulate.py when finished. Especially that thing with the speed

import threading
import time
import json

with open("config.json", "r") as fobj:
    config = json.load(fobj)

if "simulate" in config and config["simulate"]:
    from simulate import Pump
else:
    from pump import Pump

_pumps = []

for index in range(len(config["pins"])):
    _pumps.append(Pump(config["pins"][index], config["1cl_dur"][index] if (config["1cl_dur"]) == list else config["1cl_dur"]))

def _timer(delay, function):
    time.sleep(delay)
    function()

def pour(pump: int, amount: int):
    pump = _pumps[pump-1]
    pump.on()
    threading.Thread(target=lambda: _timer(amount * pump.speed, pump.off), daemon=True).start()

def check_pumps(ids: list):
    return [_pumps[_id].state() for _id in ids]

def get_pump_speeds(ids: list):
    return [_pumps[_id].speed for _id in ids]

def stop_all():
    for pump in _pumps:
        pump.off()