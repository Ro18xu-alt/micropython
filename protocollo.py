#protocollo

import utime

class ProtocolTimeout(Exception):
    pass

def read_line(usb, poll, timeout_s = 20.0):
    deadline = utime.ticks_add(utime.ticks_ms(), int(timeout_s * 1000)) 
    buf = bytearray()   # qui creo un array di byte di dimensione variabile
    while utime.ticks_diff(deadline, utime.ticks_ms()) > 0:
        if poll.poll(100):
            ch = usb.read(1)
            if ch:
                if ch == b'\n':
                    return bytes(buf)  #  converto l'array di byte variabile in un array di grandezza fissa
                buf += ch
        
    raise ProtocolTimeout('Nessun dato ricevuto entro il timeout')

def write_line(usb, testo):
    if isinstance(testo, str):
        usb.write((testo + '\n').encode('utf-8'))
    else: 
        usb.write(testo + b'\n')