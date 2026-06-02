import utime
from PID import PID
from machine import Pin, ADC, UART
from thermistor import Thermistor

#---------------------------------------
#                 INIT PINS
# --------------------------------------

ssr_pin =       Pin("B5", Pin.OUT)
adc_pin =       Pin("A0", Pin.IN)
led_green =     pyb.LED(1)
led_blue =      pyb.LED(2)
led_red =       pyb.LED(3)

#---------------------------------------
#                UART
# --------------------------------------

uart = UART(2, baudrate=115200) # PIN D5 D6
# CN9 PIN 6 / STM pin PD5 / TX
# CN9 PIN 4 / DTM pin PD6 / RX
#---------------------------------------
#                 INIT ADC
# --------------------------------------

adc_A0 = ADC(adc_pin)

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
    Kd=20,
    setpoint=35.0
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
            on_time = (out_pid / 100.0) * window

            # print("Measured Temperature: {:.2f} C".format(temperatura_attuale))
            # print("PID Output: {:.1f} %".format(out_pid))
            # print("ON Time: {:.3f}".format(on_time))
            # print()

            data_string  = f"{utime.ticks_ms()},{pid.setpoint},{temperatura_attuale:.2f},{out_pid:.1f},{on_time:.2f}" + "\n"
            #print(data_string)

            uart.write("123.6")
            #print(usb.isconnected())
            if usb.isconnected():
                # print(data_string)
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
    