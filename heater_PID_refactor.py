import utime
import pyb
from PID import PID
from machine import Pin, ADC, UART
from thermistor import Thermistor

VDD        = const(3.297)
SSR_ACCESO = const(0)
SSR_SPENTO = const(1)

#---------------------------------------
#                 INIT PINS
# --------------------------------------

ssr_pin =       Pin("B5", Pin.OUT, value=SSR_SPENTO) # CN7 pin 14
adc_pin_A0 =    Pin("A0", Pin.IN)  # CN9 pin 1
adc_pin_A1 =    Pin("C0", Pin.IN)  # CN9 pin 3
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

therm = Thermistor(pin_adc=adc_A0, beta=3485, therm_ohm=10_000, divider_ohm=10_000) # beta originale: 3485 - 3984

# --------------------------------------
#         Inizializzazione USB
# --------------------------------------

usb = pyb.USB_VCP()

#print(io_input_float.value())

def heater_PID_continue(setpoint=35, window = 1.5):
    
    pid = PID(
    Kp=6.0,
    Ki=0, 
    Kd=18,
    setpoint=setpoint
    )

    pid.output_limits = (0, 100)

    # TODO implementare kyboard

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

            if usb.isconnected():   
                datalog(f"{utime.ticks_ms()},{pid.setpoint},{temperatura_attuale:.2f},{out_pid:.1f},{on_time:.2f},{adc_A1_output},{adc_A1_read},{adc_V_read:.3f}")
            
            # # uart.write("123.6")

            # Limiti di sicurezza
            if on_time < 0:
                on_time = 0

            if on_time > window:
                on_time = window

            # SSR ON
            if on_time > 0:
                ssr_pin.value(SSR_ACCESO)
                led_red.on()
                utime.sleep(on_time)

            # SSR OFF
            off_time = window - on_time

            if off_time > 0:
                ssr_pin.value(SSR_SPENTO)
                led_red.off()
                utime.sleep(off_time)

        except KeyboardInterrupt:
            print("Interruzione da parte dell'utente")
            ssr_pin.value(SSR_SPENTO)
            return False 
        
def heater_PID_to_setpoint(setpoint=35, window = 1.5):
    
    pid = PID(
    Kp=6.0,
    Ki=0, 
    Kd=18,
    setpoint=setpoint
    )

    pid.output_limits = (0, 100)

    # TODO implementare kyboard

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

            if usb.isconnected():   
                datalog(f"{utime.ticks_ms()},{pid.setpoint},{temperatura_attuale:.2f},{out_pid:.1f},{on_time:.2f},{adc_A1_output},{adc_A1_read},{adc_V_read:.3f}")
            
            # Limiti di sicurezza
            if on_time < 0:
                on_time = 0

            if on_time > window:
                on_time = window

            # SSR ON
            if on_time > 0:
                ssr_pin.value(SSR_ACCESO)
                led_red.on()
                utime.sleep(on_time)

            # SSR OFF
            off_time = window - on_time

            if off_time > 0:
                ssr_pin.value(SSR_SPENTO)
                led_red.off()
                utime.sleep(off_time)

        except KeyboardInterrupt:
            print("Interruzione da parte dell'utente")
            ssr_pin.value(SSR_SPENTO)
            return False    
    
def datalog(*args):

    try: 
        args_converted = ','.join(str(arg) for arg in args) + '\n'
        usb.write(args_converted.encode('utf-8'))
    except Exception:
        print("Errore della funzione datalog su usb")

    