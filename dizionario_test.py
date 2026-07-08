# dizionario_test


PIN_CONFIG = {
    "A0" : "Pin("'A0'", Pin.IN, Pin.PULL_DOWN)",
    "D7" : "Pin(Pin.cpu.D7, Pin.IN, Pin.PULL_DOWN)",
    "C0" : "Pin("'C0'", Pin.IN, Pin.PULL_DOWN)",
    "D6" : "Pin(Pin.cpu.D6, Pin.IN, Pin.PULL_DOWN)",
}


# print(PIN_CONFIG["A0"]["obj"])

# for name_pin in PIN_CONFIG:
#     print(PIN_CONFIG[name_pin]["obj"])
nomi = list(PIN_CONFIG.keys())
print(nomi)

for driver_nome in nomi:
    pin = PIN_CONFIG[driver_nome]
    