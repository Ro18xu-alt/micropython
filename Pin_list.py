from machine import Pin

print("--- PIN DISPONIBILI SULLA CPU ---")
# Questo ti mostra tutti i nomi nativi (es. PA0, PA1, PB0...) accettati dalla scheda
nomi_cpu = dir(Pin.cpu)
print(", ".join(nomi_cpu))

print("\n" + "="*40 + "\n")

print("--- PIN MAPPATI COME BOARD (SERIGRAFIA) ---")
# Questo ti mostra se il firmware supporta i nomi "stile Arduino" (es. A0, D6...)
nomi_board = dir(Pin.board)
print(", ".join(nomi_board))