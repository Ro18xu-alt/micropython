#PC-UART
from contextlib import contextmanager
import serial
import time
import json

baudrate = 9600
port = "COM28"
timeout = 20

connessioni_attese = (('A0', 'D7'), ('D7', 'A0'))


class SerialComm:
    
    def __init__(self, port="COM28", baudrate=9600, timeout=5) -> None:
        self.port = port
        self.baudrate=baudrate
        self.timeout=timeout
        self._ser = None
        
    def __enter__(self):
        self._ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._ser:
            self._ser.close()
        print("Chiusura dell'interfaccia seriale")

    def read_line(self, timeout=20):
        deadline = time.time() + timeout
        buf = bytearray()
        while time.time() < deadline:
            ch = self._ser.read(1)
            if ch:
                if ch == b'\n':
                    return bytes(buf)
                buf += ch
                
        raise TimeoutError("Nessun messaggio o formattazione errata")  

    def handshake(self, timeout=20):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                line = self.read_line(timeout=2)
            except TimeoutError:
                continue
            if line.strip() == b"READY":
                print("Handshake success")
                return
        raise TimeoutError("Handshake fallito")

def valida_harness(connessioni_rilevate, connessioni_attese):
    rilevate_set = set()
    for a,b  in connessioni_rilevate:
        #print(a, b)
        rilevate_set.add(frozenset((a, b)))
        
        
    attese_set = {frozenset(coppie) for coppie in connessioni_attese}
    #print(type(attese_set), attese_set)
    mancanti = attese_set - rilevate_set
    inattese = rilevate_set - attese_set
    
    return mancanti, inattese
        
        
def main():
    print("PC-UART")
    
    with SerialComm() as s:
        
        s.handshake()
        s._ser.write(b"HARNESS TEST\n")
        #s.write(b"ECHO\n")
        # time.sleep(0.02)
        # s._ser.write(b"prova ECHOooooooo\n")
        
        line_raw = s.read_line().decode('utf-8')
        #list(line)
        # print(f"stampo line: {line}")
        # print(f"stampo type line : {type(line)}")
        try:
            connessioni_rilevate = [tuple(coppia) for coppia in json.loads(line_raw)]
        except Exception:
            raise ValueError("Errore nella conversione del file json")
        
        mancanti, inattese = valida_harness(connessioni_rilevate=connessioni_rilevate, connessioni_attese=connessioni_attese)

        print(mancanti)
        print(f"connessioni inattese: {inattese}")
    pass

main()