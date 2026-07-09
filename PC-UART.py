#PC-UART
from contextlib import contextmanager
import serial
import time
import json
from colorama import Fore

baudrate = 9600
port = "COM28"
timeout = 20

iso_spi_fault_u212_pin = (('A0', 'D51'), ('D51', 'A0'), ("D53", 'A2'), ('A2', 'D53'), ("D54", "A3"), ('A3', 'D54'), ("A1", "D52"), ("A1", "D52"))
iso_spi_fault_u212_dizionario = {
    "A0" : "SX J1INA_1 ISOB N",
    "D51": "DX J1OUTA_1 ISOA N",
    
    "A1":  "SX J1INA_2 ISOB P",
    "D52": "DX J1OUTA_2 ISOA P",
    
    "A2":  "SX J1INB_3 FAULT IN",
    "D53": "DX J1OUTA_3 FAULT OUT",
    
    "A3" : "SX J1INB_4 FAULT RTN IN",
    "D54": "DX J1OUTB_4 FAULT RTN OUT"
    
    
}

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
        print("\n\nChiusura dell'interfaccia seriale")

    def read_line(self, timeout=20):
        deadline = time.time() + timeout
        buf = bytearray()
        while time.time() < deadline:
            ch = self._ser.read(1) #type: ignore
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

def stampa_report(mancanti, inattese, dizionario: dict):

    if not mancanti and not inattese:
        print(f"\n\n{Fore.GREEN}OK -  HARNESS VALIDO{Fore.RESET}, tutte le connessioni corrispondono")
        return     
    else:
        print(f"\n\n{Fore.RED}KO - HARNESS NON VALIDO{Fore.RESET}, controllare le connessioni mancanti o errate")
        if mancanti:
            print(f"\nConnessioni {Fore.RED}MANCANTI{Fore.RESET}: {len(mancanti)}")
            for c in sorted(mancanti, key=sorted):
                a, b = c
                print(f"{(dizionario.get(a, a)).center(5)}  <->  {dizionario.get(b, b).center(5)}")
        if inattese :
            print(f"\nConnessioni {Fore.YELLOW}INATTESE{Fore.RESET}: {len(inattese)}")
            for c in sorted(inattese, key=sorted):
                a, b = c
                print(f"! {dizionario.get(a, a).center(5)}  <->  {dizionario.get(b, b).center(5)}") 
        
        
def main():
    print("PC-UART")
    
    with SerialComm() as s:
        
        s.handshake()
        s._ser.write(b"HARNESS TEST\n") #type: ignore
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
        
        mancanti, inattese = valida_harness(connessioni_rilevate=connessioni_rilevate, connessioni_attese=iso_spi_fault_u212_pin, )
        stampa_report(mancanti, inattese, iso_spi_fault_u212_dizionario)
                
    pass

main()