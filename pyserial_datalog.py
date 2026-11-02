import serial, csv, time, threading 
from collections import deque
import serial.tools.list_ports

SETPOINT = 80

def trova_porta_seriale():
    """Cerca la porta della NUCELO tramite VID/PID"""
    for p in serial.tools.list_ports.comports():
        if p.vid == 0xf055: # mi connetto alla NUCELO ST tramite VID specifico 
            return p.device

    return None

def apri_seriale(timeout=10):
    #log = logging.getLogger("harness")
    start_time = time.time()
    while time.time() - start_time < timeout:
        porta = trova_porta_seriale()

        if porta: 
            try:
                ser = serial.Serial(porta, 115200, timeout=2)
                #logging.getLogger("harness").info(f"Inizializzata porta {porta}")
               
                return ser
            except serial.SerialException:
                pass # retry

        time.sleep(0.5)

    raise TimeoutError("NUCELO non rilevata")

serial_port = apri_seriale()
#serial_port = "/dev/ttyACM1"
baudrate = 115200

time_now = time.strftime(f"%d_%m_%Y__%H_%M_%S", time.gmtime())
file_output=f"{time_now}_PID_datalog.csv"
header = ["timestamp_pc","ticks (ms)", "setpoint (°C)", "temperature_measured (°C)", "out_pid (%)", "on_time (s)", "SensorStrip_trig","ADC_A1_raw","ADC_A1_V"]



def serial_reader(serial_port, header, xs, ys1, ys2, lock, file_output, baudrate=115200, timeout=2):
    try: 
       #with serial.Serial(serial_port, baudrate=baudrate, timeout=timeout) as ser, \
        with serial_port as ser, \
            open(file_output, 'w', newline='', encoding='utf-8') as file_w:
            
            ser.write(('\x03' + '\n').encode('utf-8'))
            ser.write(("import heater_PID" +'\n').encode("utf-8"))
            ser.write((f"heater_PID.heater_PID_to_setpoint(setpoint={SETPOINT})" + '\n').encode('utf-8'))
            writer = csv.writer(file_w)
            writer.writerow(header) # scrivo l'intestazione del file CSV

            while True:
                line_bytes = ser.readline() # Controlla se nel buffer c'è stringa di testo inviata dalla nucelo
                if not line_bytes:
                    continue
                
                try:   
                    line = line_bytes.decode('utf-8').strip() # decodifica la stringa ricevuta dalla nucleo
                    if not line: 
                        continue
                                        
                    dati = line.split(',')
                    if len(dati) + 1 != len(header):
                        print(f"Stringa incompleta: {dati}")
                        continue

                    timestamp_pc = time.strftime("%Y-%m-%d %H:%M:%S")
                    dati.insert(0, timestamp_pc)
                    writer.writerow(dati)
                    file_w.flush()
                    
                    print(f"Scritta riga: {dati}")

                    with lock:        
                        xs.append(time.time() - t0)
                        ys1.append(float(dati[3]))
                        ys2.append(float(dati[5]))
                
                except (UnicodeDecodeError, ValueError, IndexError) as e:
                     print(f"Riga scartata {e}, {line_bytes!r}")
                     
    except serial.SerialException as e:
        print(f"Si è verificato un errore nella seriale: {e}")
    except OSError as e:
        print(f"Errore apertura file/porta {e}")     
        
xs = deque(maxlen=600)
ys1 = deque(maxlen=600)
ys2 = deque(maxlen=600)
lock = threading.Lock()
t0 = time.time()

th = threading.Thread(
    target=serial_reader,
    args= (serial_port, header, xs, ys1, ys2, lock, file_output, baudrate),
    daemon=True
)
th.start()

import matplotlib.pyplot as plt        
plt.ion()
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
line_plot1, = ax1.plot([],[], color='C0')
line_plot2, = ax2.plot([],[], color= 'C1')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Temp [°C]')    
ax2.set_ylabel('Activation time [s]')

try:
    while True:  
        with lock:
            x = list(xs)
            y1 = list(ys1)
            y2 = list(ys2)
            
        if x:           
            line_plot1.set_data(list(xs), list(ys1))
            line_plot2.set_data(list(xs), list(ys2))
            ax1.relim(); ax1.autoscale_view()
            ax2.relim(); ax2.autoscale_view()

        plt.pause(0.2)
except KeyboardInterrupt:
    serial_port.write(("\x03" + '\n').encode('utf-8'))
    print("Keyboard interrupt, programma terminato")
                    