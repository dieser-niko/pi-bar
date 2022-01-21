Please use gpiozero, you should use gpiozero.OutputDevice(pin[int], active_high=False, initial_value=False)
Then just relay.toggle()/on()/off()

the config.json has som config.
potential for different speeds: what if the speed can be a value or a list?