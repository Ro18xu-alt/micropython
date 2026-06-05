import serial
import csv
import time

time_now = time.strftime(f"%d_%m_%Y__%H_%M_%S", time.gmtime())
serial_port = "COM28"
#serial_port = "/dev/ttyACM1"
baudrate = 115200
file_output=f"{time_now}_PID_datalog.csv"
header = ["timestamp_pc","ticks (ms)", "setpoint (°C)", "temperature_measured (°C)", "out_pid (%)", "on_time (s)", "SensorStrip_trig","ADC_A1_raw","ADC_A1_V"]

#------------------
#     DEBUG
#------------------

# with open(file_output, 'w', newline='') as f:
#     writer = csv.writer(f)

#     writer.writerow(header)

# print(file_output)



def csv_writer(serial_port, header, baudrate=9600, timeout=2):
    try: 
        with serial.Serial(serial_port, baudrate=baudrate, timeout=timeout) as ser, \
            open(file_output, 'w', newline='', encoding='utf-8') as file_w:
          
            writer = csv.writer(file_w)
            # scrivo l'intestazione del file CSV
            writer.writerow(header)

            while True:
                
                line_bytes = ser.readline()
                
                # if ser.in_waiting > 0:
                if line_bytes:
                    # legge stringa ricevuta dalla nucelo
                    line = line_bytes.decode('utf-8').strip()
                    
                    if line:                       
                        dati = line.split(',')
                        
                        if len(dati) + 1 == len(header):

                            timestamp_pc = time.strftime("%Y-%m-%d %H:%M:%S")
                            #print(type(timestamp_pc))
                            dati.insert(0, timestamp_pc)

                            writer.writerow(dati)
                            file_w.flush()

                            print(f"Scritto riga: {dati}")
                        else:
                            print(f"Stringa incompleta: {dati}")


    except KeyboardInterrupt:
        print(f"datalog interrotto dall'utente")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
                
            
csv_writer(serial_port, header, baudrate, 2)