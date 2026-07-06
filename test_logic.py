# test_logic.py

from pyb import Pin
import utime

def test_pin(pins_dict: dict, settling_ms=20):
    nomi_pin = list(pins_dict.keys())
    connessioni_trovate = []

    for p in pins_dict.values():
        p.init(p.IN, p.PULL_DOWN)

    for driver_output in nomi_pin:
        driver = pins_dict[driver_output]
        driver.init(driver.OUT_PP)
        driver.value(1)
        utime.sleep_ms(settling_ms)

        for driver_input in pins_dict:
            if driver_output == driver_input:
                continue
            if pins_dict[driver_input].value() == 1:
                connessioni_trovate.append((driver_output, driver_input))

        driver.value(0)
        driver.init(driver.IN, driver.PULL_DOWN)
        utime.sleep_ms(settling_ms)

    return connessioni_trovate    
    