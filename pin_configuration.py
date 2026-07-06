# pin_configuration.py
from pyb import Pin

PIN_CONFIG = {
    "A0" : Pin("A0", Pin.IN, Pin.PULL_DOWN),
    "D7" : Pin(Pin.cpu.D7, Pin.IN, Pin.PULL_DOWN),
    "C0" : Pin("C0", Pin.IN, Pin.PULL_DOWN),
    "D6" : Pin(Pin.cpu.D6, Pin.IN, Pin.PULL_DOWN),
}

def reset_pin_state():
    for p in PIN_CONFIG.values():
        p.init(p.IN, p.PULL_DOWN)

        