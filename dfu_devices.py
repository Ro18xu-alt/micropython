import pyusb.core

# STM32 DFU VID/PID standard
dev = usb.core.find(idVendor=0x0483, idProduct=0xDF11)

if dev is None:
    print("STM32 DFU non trovato")
else:
    print("STM32 DFU trovato")