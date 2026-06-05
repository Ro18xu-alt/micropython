import utime
import pyb
from PID import PID
from machine import Pin, ADC, UART
from thermistor import Thermistor

VDD = 3.297

#---------------------------------------
#                 INIT PINS
# --------------------------------------

ssr_pin =       Pin("B5", Pin.OUT)
adc_pin_A0 =    Pin("A0", Pin.IN)
adc_pin_A1 =    Pin("C0", Pin.IN)
led_green =     pyb.LED(1)
led_blue =      pyb.LED(2)
led_red =       pyb.LED(3)

#---------------------------------------
#                UART
# --------------------------------------

# uart = UART(2, baudrate=115200) # PIN D5 D6
# CN9 PIN 6 / STM pin PD5 / TX
# CN9 PIN 4 / DTM pin PD6 / RX
#---------------------------------------
#                 INIT ADC
# --------------------------------------

adc_A0 = ADC(adc_pin_A0)
adc_A1 = ADC(adc_pin_A1)

#---------------------------------------
#                 INIT thermistor
# --------------------------------------

therm = Thermistor(pin_adc=adc_A0, beta=3435, therm_ohm=10_000, divider_ohm=10_000)

#---------------------------------------
#            CONFIGURAZIONE PID 
# --------------------------------------

# Kp, Ki, Kd vanno pesati in base al sistema.
# output_limits: il PWM di MicroPython accetta valori da 0 a 65535.

pid = PID(
    Kp=6.0,
    Ki=0, # provare ad inserire 1 al parametro
    Kd=18,
    setpoint=60
)

pid.output_limits = (0, 100)

#---------------------------------------
#          finestra temporale 
# --------------------------------------

window = 1.5

# --------------------------------------
#         Inizializzazione USB
# --------------------------------------

usb = pyb.USB_VCP()
ssr_pin.on()

#print(io_input_float.value())

def heater_PID():

    # TODO implementare kyboard
    # TODO implementare datalog 

    print("Chiamata funzione heater_PID(), ctrl+C per interrompere")

    while True:
        try:
            
            # Lettura temperatura
            temperatura_attuale = therm.read_temperature_celsius()

            # Calcolo PID
            out_pid = pid(temperatura_attuale)

            # Calcolo tempo ON
            on_time = (out_pid / 100.0) * window # type:ignore

            # print("Measured Temperature: {:.2f} C".format(temperatura_attuale))
            # print("PID Output: {:.1f} %".format(out_pid))
            # print("ON Time: {:.3f}".format(on_time))
            # print()
            
            adc_A1_read = adc_A1.read_u16() >> 4
            adc_A1_percent = ( adc_A1_read * 100 ) / 4095
            adc_V_read = (adc_A1_read / 4095) * VDD
            
            if adc_A1_percent >= 70:
                adc_A1_output = "1"
            else: 
                adc_A1_output = "0"
                
            # print(adc_A1_read)
            # print(adc_A1_percent)
            # print(adc_A1_output)

            data_string  = f"{utime.ticks_ms()},{pid.setpoint},{temperatura_attuale:.2f},{out_pid:.1f},{on_time:.2f},{adc_A1_output},{adc_A1_read},{adc_V_read:.3f}" + "\n"
            #print(data_string)

            # uart.write("123.6")
            #print(usb.isconnected())
            if usb.isconnected():
                #print(data_string)
                usb.write(data_string.encode('utf-8') )
                
            
            
            # Limiti di sicurezza
            if on_time < 0:
                on_time = 0

            if on_time > window:
                on_time = window

            # SSR ON
            if on_time > 0:
                ssr_pin.off()
                led_red.on()
                utime.sleep(on_time)

            # SSR OFF
            off_time = window - on_time

            if off_time > 0:
                ssr_pin.on()
                led_red.off()
                utime.sleep(off_time)

        except KeyboardInterrupt:
            print("Interruzione da parte dell'utente")
            return False    
    