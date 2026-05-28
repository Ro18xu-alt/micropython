import time
from machine import Pin, ADC, PWM
from PID import PID
#from simple_pid import PID
from thermistor import Thermistor

ssr_pin = Pin("B5", Pin.OUT)
ssr_pwm = PWM(ssr_pin)
ssr_pwm.freq(2)

adc_pin = Pin("A0", Pin.IN)
pin_led = Pin("LED_RED", Pin.OUT)
adc = ADC(adc_pin)

therm = Thermistor(pin_adc= adc,beta=3435, therm_ohm=10_000, divider_ohm=10_000)

# --- CONFIGURAZIONE PID ---
# Kp, Ki, Kd vanno sintonizzati in base al tuo sistema reale.
# output_limits: il PWM di MicroPython accetta valori da 0 a 65535.
pid = PID(Kp=450.0, Ki=250, Kd=1000.0, setpoint=35.0)
pid.output_limits = (0, 65535)  # Canale PWM standard MicroPython

while True:
    # print("Measured Voltage:      " + str(therm.read_voltage()) + " V")
    # print("Measured Resistance:   " + str(therm.read_resistance()) + " Ohm")
    print("Measured Temperature:  " + str(therm.read_temperature_celsius()) + " C")
    print("")
    
    temperatura_attuale = therm.read_temperature_celsius()
    
    output_pwm = pid(temperatura_attuale)
    
    ssr_pwm.duty_u16(int(output_pwm))

    time.sleep_ms(100)

