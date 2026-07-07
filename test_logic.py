# test_logic.py

from pyb import Pin
import utime

def test_pin(pins_dict: dict, settling_ms=100):
    nomi_pin = list(pins_dict.keys())
    connessioni_trovate = []

    for p in pins_dict.values():
        p.init(p.IN, p.PULL_DOWN)

    for driver_output in nomi_pin:
        driver = pins_dict[driver_output]
        #print(driver)
        driver.init(driver.OUT_PP)
        driver.value(1)
        utime.sleep_ms(settling_ms)

        for driver_input in pins_dict:
            #print(f"driver output: {driver_output} driver input: {driver_input}")
            if driver_output == driver_input:
                continue
            if pins_dict[driver_input].value() == 1:
                #print(f"driver input valuore 1: {driver_input}")
                connessioni_trovate.append((driver_output, driver_input))

        driver.value(0)
        driver.init(driver.IN, driver.PULL_DOWN)
        utime.sleep_ms(settling_ms)

    return connessioni_trovate    
    