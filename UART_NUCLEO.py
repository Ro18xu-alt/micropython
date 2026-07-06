import micropython
import pyb
from pyb import Pin
import utime
import select
from protocollo import ProtocolTimeout, read_line, write_line
from pin_configuration import PIN_CONFIG, reset_pin_state
from test_logic import test_pin

led_green = pyb.LED(1)
led_blue  = pyb.LED(2)
led_red = pyb.LED(3)
# pin_out_1 = Pin("A0", Pin.OUT_PP)                   # CN9_1
# pin_out_2 = Pin("C0", Pin.OUT_PP)                   # CN9_3

# pin_in_1 = Pin(Pin.cpu.D7, Pin.IN, Pin.PULL_DOWN)  # CN9_2
# pin_in_2 = Pin(Pin.cpu.D6, Pin.IN, Pin.PULL_DOWN)  # CN9_4

# pin_dict_test_1 = {
#     "Molex J1.2 ---> microFit J8.3" : (pin_out_1, pin_in_1),
#     "Molex J1.1 ---> RisoConnect J8.4" : (pin_out_2, pin_in_2)
# }

# input_pin_alias = {
#     "D7" : pin_in_1,
#     "D6" : pin_in_2
# }

# output_pin_alias = {
#     "A0" : pin_out_1,
#     "C0" : pin_out_2,
# }


#uart = UART(1, baudrate=115200) # PIN D5 D6

usb = pyb.USB_VCP()

# usb è il tuo oggetto USB VCP (pyb.USB_VCP())
poll = select.poll()            # qui creo il sorvegliane, è vuoto e così non ha funzioni da controllare
poll.register(usb, select.POLLIN) #  qui indico quale evento controllare - POLLIN sifgnifica avvisami
 # non appena c'è un elemento da leggere all'ingresso 
 # poll.poll(100) è una chiamata che controlla, dice di aspettare fino a 100ms per un evento in entrata
 # in alernativa risponde comunque
 # Lista non vuota TRUE- ha almeno un dato da leggere, possiamo leggere subito
 # lista vuota FALSE - non ci sono dati da leggere e allo scadere dei 100ms prosegue 
# se dovessero arrivare più byte e il mio ciclo gestisce un byte alla volta questi vengono conservati nella
# buffer e vengono gestiti ciclo dopo ciclo, non andrebbero persi.
# restano nel buffer hardware/software della VCP 
# poll viene quindi triggherato ad ogni byte presente nel buffer, non devo sincronizzare le velocità 

# print(usb.isconnected())
# def read_byte():
#     while True:
#         if usb.isconnected():
#             bytes = usb.readline()

#             stringa_= str(bytes, 'utf-8')
#             #print(type(stringa_))

#             print(f"eseguo un print della stringa {stringa_}")
#             if stringa_[:1] == 'o':
#                 print(f"Ho ricevuo un pin di output procedo alla decodifica")
#             else:
#                 print(bytes)
            
#         else:
#             print("No Connection")
#         utime.sleep(1)
    
# def read_line(timeout = 20.0):
#     """Legge una riga terminata da \n, bloccante."""
#     deadline = utime.time() + timeout
#     buf = bytearray()
#     while utime.time() < deadline:
#         if poll.poll(100):          # timeout 100ms, non-busy wait
#             ch = usb.read(1)
#             if ch:
#                 if ch == b'\n':
#                     return bytes(buf)
#                 buf += ch
#     raise TimeoutError("Tempo di attesa massimo superato")
    
# def pin_control():
    
#     while not usb.isconnected():
#         pass
#         #print("Connected")
    
#     usb.write(b"READY\n")
        
#     while True:
#         line = read_line()
#         #bytes = usb.read()

#         cmd = str(line, 'utf-8').strip()

#         # print(stringa_)
#         # print(match_)
#         # print(type(stringa_))
        
#         if cmd == 'END':
#             print("End test")
#             break

#         ok = test_pin(cmd)
#         risposta = "{}:{}\n".format(cmd, "OK" if ok else 'FAIL')
#         usb.write(risposta.encode('utf-8'))
        
           
# def test_pin(nome_pin):

    
#     parts = nome_pin.split('_')

#     pin_out_str = parts[0]
#     pin_in_str = parts[1]

#     #print(pin_out, pin_in)
#     pin_out = output_pin_alias.get(pin_out_str)
#     pin_in = input_pin_alias.get(pin_in_str)
#     pin_out.value(1)

#     if pin_in.value() == 1:
#         pin_out.value(0)
#         utime.sleep(0.5)
#         return True
#     else:
#         pin_out.value(0)
#         utime.sleep(0.5)
#         return False
    
def gestisci_comando(cmd):
    
    reset_pin_state()

    if cmd == 'START':
        corti = test_pin(PIN_CONFIG)   
        if not corti:
            return "SHORT:NONE"
        coppie = ",".join("{}-{}".format(a,b) for a, b in corti)
        return "SHORT:FOUND:{}".format(coppie) 
    
    else:
        return "ERR: comando sconosciuto {}".format(cmd)
    
def test():

    while not usb.isconnected():
        pass
    write_line(usb, "READY")

    while True:
        try:
            line = read_line(usb, poll, timeout_s=20)
        except ProtocolTimeout:
            continue

        cmd = str(line, 'utf-8').strip()

        if cmd == "END":
            reset_pin_state()
            break

        risposta = gestisci_comando(cmd)
        write_line(usb, risposta)
        print(risposta)

def handshake():
    while not usb.isconnected():
        pass
    write_line(usb, "READY")

def echo():
    while not usb.isconnected():
        pass
    write_line(usb, "READY")

    testo = read_line(usb, poll)
    
    write_line(usb, testo)

def gestisci_lista_comandi():
    handshake()

    cmd = read_line(usb, poll)

    if cmd == b"1":
        write_line(usb, "Questo è il caso 1")

    elif cmd == b"2":
        write_line(usb, "Questo è il caso 2")


    
