# pin_configuration.py
# ============================================================
# PIN_CONFIG - NUCLEO-H563ZI (STM32H563ZIT6)
# Riferimento: UM3115 Rev 3 - Tabelle 21, 22, 23, 24
# Chiave  = label ST Zio / ARDUINO (serigrafia board)
# Valore  = Pin CPU in IN, PULL_DOWN (listener di default)
# Commento = CPU | connettore-pin | funzione STM32
#
# NOTA DUP: label marcate # DUP condividono lo stesso pin CPU
#           di un'altra label. Nella lista di scansione del
#           test_pin_universale il pin CPU va incluso UNA SOLA
#           volta per evitare falsi corto-circuiti.
# ============================================================

from pyb import Pin
import utime
def _in(cpu):
    return Pin(cpu, Pin.IN, Pin.PULL_DOWN)

PIN_CONFIG = {

    # # ========== CN7 (Tab.21) ==========
    "D16": _in(Pin.cpu.C6),   # PC6  | CN7-1  | I2S_A_MCK  OK
    "D15": _in(Pin.cpu.B8),   # PB8  | CN7-2  | I2C_A_SCL  OK
    #"D17": _in(Pin.cpu.B15),  # PB15 | CN7-3  | I2S_A_SD  (cond. RMII_TXD1 se JP6 ON)
    #"D14": _in(Pin.cpu.B9),   # PB9  | CN7-4  | I2C_A_SDA
    #"D18": _in(Pin.cpu.B13),  # PB13 | CN7-5  | I2S_A_CK  (cond. UCPD_CC1)
    # CN7-6  = VREFP
    #"D19": _in(Pin.cpu.B12),  # PB12 | CN7-7  | I2S_A_WS
    # CN7-8  = GND
    #"D20": _in(Pin.cpu.A15),  # PA15 | CN7-9  | I2S_B_WS
    #"D13": _in(Pin.cpu.A5),   # PA5  | CN7-10 | SPI_A_SCK (anche LD1) 
    "D21": _in(Pin.cpu.C7),   # PC7  | CN7-11 | I2S_B_MCK #OK
    "D12": _in(Pin.cpu.G9),   # PG9  | CN7-12 | SPI_A_MISO #OK
    #"D22": _in(Pin.cpu.B5),   # PB5  | CN7-13 | I2S_B_SD/SPI1_MOSI 
    #"D11": _in(Pin.cpu.B5),   # PB5  | CN7-14 | SPI1_MOSI          # DUP di D22
    #"D23": _in(Pin.cpu.B3),   # PB3  | CN7-15 | I2S_B_CK/SPI1_SCK (cond. SWO)
    "D10": _in(Pin.cpu.D14),  # PD14 | CN7-16 | SPI_A_CS/TIM4_CH3 # OK
    "D24": _in(Pin.cpu.G10),  # PG10 | CN7-17 | SPI_B_NSS # OK
    "D9":  _in(Pin.cpu.D15),  # PD15 | CN7-18 | TIM4_CH4 
     "D25": _in(Pin.cpu.B4),   # PB4  | CN7-19 | SPI_B_MISO
     "D8":  _in(Pin.cpu.F3),   # PF3  | CN7-20 | IO

    # ========== CN8 (Tab.22) ==========
    # # CN8-1  = NC
     "D43": _in(Pin.cpu.C8),   # PC8  | CN8-2  | SDMMC_D0
     # CN8-3  = IOREF ; CN8-5 = NRST ; CN8-7 = 3V3 ; CN8-9 = 5V
     # CN8-11 = GND ; CN8-13 = GND ; CN8-15 = VIN
     "D44": _in(Pin.cpu.C9),   # PC9  | CN8-4  | SDMMC_D1/I2S_A_CKIN
     "D45": _in(Pin.cpu.C10),  # PC10 | CN8-6  | SDMMC_D2
     "D46": _in(Pin.cpu.C11),  # PC11 | CN8-8  | SDMMC_D3
     "D47": _in(Pin.cpu.C12),  # PC12 | CN8-10 | SDMMC_CK
     "D48": _in(Pin.cpu.D2),   # PD2  | CN8-12 | SDMMC_CMD
     "D49": _in(Pin.cpu.G2),   # PG2  | CN8-14 | IO
     "D50": _in(Pin.cpu.G3),   # PG3  | CN8-16 | IO

    # ========== CN9 (Tab.23) ==========
    "A0":  _in(Pin.cpu.A6),   # PA6  | CN9-1  | ADC12_INP3
    "D51": _in(Pin.cpu.D7),   # PD7  | CN9-2  | USART2_SCLK
    "A1":  _in(Pin.cpu.C0),   # PC0  | CN9-3  | ADC12_INP10
    "D52": _in(Pin.cpu.D6),   # PD6  | CN9-4  | USART2_RX
    "A2":  _in(Pin.cpu.C3),   # PC3  | CN9-5  | ADC12_INP13
    "D53": _in(Pin.cpu.D5),   # PD5  | CN9-6  | USART2_TX
    "A3":  _in(Pin.cpu.B1),   # PB1  | CN9-7  | ADC12_INP5
    "D54": _in(Pin.cpu.D4),   # PD4  | CN9-8  | USART2_RTS
    "A4":  _in(Pin.cpu.C2),   # PC2  | CN9-9  | ADC12_INP12 (o PB9)
    "D55": _in(Pin.cpu.D3),   # PD3  | CN9-10 | USART2_CTS
    "A5":  _in(Pin.cpu.F11),  # PF11 | CN9-11 | ADC1_INP2 (o PB8)
    # CN9-12 = GND
    "D72": _in(Pin.cpu.B2),   # PB2  | CN9-13 | IO
    "D56": _in(Pin.cpu.E2),   # PE2  | CN9-14 | SAI_A_MCLK
    "D71": _in(Pin.cpu.E9),   # PE9  | CN9-15 | IO
    "D57": _in(Pin.cpu.E4),   # PE4  | CN9-16 | SAI_A_FS
    "D70": _in(Pin.cpu.F2),   # PF2  | CN9-17 | I2C_B/SMBA
    "D58": _in(Pin.cpu.E5),   # PE5  | CN9-18 | SAI_A_SCK
    "D69": _in(Pin.cpu.F1),   # PF1  | CN9-19 | I2C_B_SCL
    "D59": _in(Pin.cpu.E6),   # PE6  | CN9-20 | SAI_A_SD
    "D68": _in(Pin.cpu.F0),   # PF0  | CN9-21 | I2C_B_SDA
    "D60": _in(Pin.cpu.E3),   # PE3  | CN9-22 | SAI_B_SD
    # CN9-23 = GND
    "D61": _in(Pin.cpu.F8),   # PF8  | CN9-24 | SAI_B_SCK
    "D67": _in(Pin.cpu.D0),   # PD0  | CN9-25 | CAN_RX
    "D62": _in(Pin.cpu.F7),   # PF7  | CN9-26 | SAI_B_MCLK
    "D66": _in(Pin.cpu.D1),   # PD1  | CN9-27 | CAN_TX
    "D63": _in(Pin.cpu.F9),   # PF9  | CN9-28 | SAI_B_FS
    "D65": _in(Pin.cpu.G0),   # PG0  | CN9-29 | IO
    "D64": _in(Pin.cpu.G1),   # PG1  | CN9-30 | IO

    # ========== CN10 (Tab.24) ==========
    # CN10-1 = AVDD ; CN10-3 = AGND ; CN10-5 = GND
    "D7":  _in(Pin.cpu.G12),  # PG12 | CN10-2  | IO
    #"D6":  _in(Pin.cpu.E9),   # PE9  | CN10-4  | TIM1_CH1          # DUP di D71
    "A6":  _in(Pin.cpu.F12),  # PF12 | CN10-7  | ADC1_INP6
    "D5":  _in(Pin.cpu.E11),  # PE11 | CN10-6  | TIM1_CH2
    "A7":  _in(Pin.cpu.F13),  # PF13 | CN10-9  | ADC2_INP2
    "D4":  _in(Pin.cpu.E14),  # PE14 | CN10-8  | IO
    "A8":  _in(Pin.cpu.F14),  # PF14 | CN10-11 | ADC2_INP6
    "D3":  _in(Pin.cpu.E13),  # PE13 | CN10-10 | TIM1_CH3
    "D26": _in(Pin.cpu.G6),   # PG6  | CN10-13 | QSPI_BCS
    "D2":  _in(Pin.cpu.G14),  # PG14 | CN10-12 | IO
    #"D27": _in(Pin.cpu.B2),   # PB2  | CN10-15 | QSPI_CLK          # DUP di D72
    "D1":  _in(Pin.cpu.B6),   # PB6  | CN10-14 | USART_A_TX/LPUART1
    # CN10-17 = GND
    "D0":  _in(Pin.cpu.B7),   # PB7  | CN10-16 | USART_A_RX/LPUART1
    "D28": _in(Pin.cpu.D13),  # PD13 | CN10-19 | QSPI_BK1_IO3
    "D42": _in(Pin.cpu.E8),   # PE8  | CN10-18 | TIM1_CH1N
    "D29": _in(Pin.cpu.D12),  # PD12 | CN10-21 | QSPI_BK1_IO1
    "D41": _in(Pin.cpu.E7),   # PE7  | CN10-20 | TIM1_ETR
    "D30": _in(Pin.cpu.D11),  # PD11 | CN10-23 | QSPI_BK1_IO0
    # CN10-22 = GND
    #"D31": _in(Pin.cpu.E2),   # PE2  | CN10-25 | QSPI_BK1_IO2      # DUP di D56
    "D40": _in(Pin.cpu.E10),  # PE10 | CN10-24 | TIM1_CH2N
    "D39": _in(Pin.cpu.E12),  # PE12 | CN10-26 | TIM1_CH3N
    # CN10-27 = GND
    "D32": _in(Pin.cpu.A0),   # PA0  | CN10-29 | TIM2_CH1
    #"D38": _in(Pin.cpu.E6),   # PE6  | CN10-28 | TIM1_BKIN2        # DUP di D59
    "D33": _in(Pin.cpu.B0),   # PB0  | CN10-31 | TIM3_CH3
    "D37": _in(Pin.cpu.E15),  # PE15 | CN10-30 | TIM1_BKIN1
    "D34": _in(Pin.cpu.E0),   # PE0  | CN10-33 | TIM4_ETR
    "D36": _in(Pin.cpu.B10),  # PB10 | CN10-32 | TIM2_CH3
    "D35": _in(Pin.cpu.A3),   # PA3  | CN10-34 | TIM2_CH4
}

def reset_pin_state():
    for p in PIN_CONFIG.values():
        p.init(p.IN, p.PULL_DOWN)
        utime.sleep_ms(1)

        

