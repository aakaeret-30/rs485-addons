import serial
import time
import binascii

SERIAL_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AU0YA7RI-if00-port0"
BAUDRATE = 9600

def beregn_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder='little')

print(f"Starter dybsscanning på port: {SERIAL_PORT}", flush=True)
try:
    ser = serial.Serial(
        port=SERIAL_PORT, baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE, timeout=0.2
    )
except Exception as e:
    print(f"Kunne ikke åbne port: {e}", flush=True)
    exit(1)

# Vi scanner en blok af gangen for at finde live-værdierne
# Vi starter med at scanne adresse 20 til 70 (omkring de 40)
start_adresse = 150
antal_adresser = 50

while True:
    print(f"\n--- Starter scanningsrunde fra adresse {start_adresse} til {start_adresse + antal_adresser} ---", flush=True)
    for adr in range(start_adresse, start_adresse + antal_adresser):
        # Byg Modbus-pakke til ID 1, Func 03, 1 register
        pakke_data = bytes([1, 3]) + adr.to_bytes(2, byteorder='big') + bytes([0, 1])
        fuld_pakke = pakke_data + beregn_crc(pakke_data)
        
        ser.write(fuld_pakke)
        time.sleep(0.06)  # Hurtig afvikling
        
        if ser.in_waiting > 0:
            svar = ser.read(ser.in_waiting)
            if len(svar) >= 5 and svar[1] == 3:
                # Konverter de to data-bytes til et tal
                val = int.from_bytes(svar[3:5], byteorder='big', signed=True)
                # Vi udskriver KUN hvis værdien IKKE er 0 eller 1, så vi slipper for støjen!
                if val != 0 and val != 1:
                    print(f"👉 Adresse {adr} svarede med rå værdi: {val} (svarende til {val*0.1:.1f})", flush=True)
                    
    time.sleep(5)
