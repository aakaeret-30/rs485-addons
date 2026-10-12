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

print(f"Starter automatisk Modbus-scanning på port: {SERIAL_PORT}", flush=True)
try:
    ser = serial.Serial(
        port=SERIAL_PORT, baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE, timeout=0.3  # Hurtig timeout til scanning
    )
except Exception as e:
    print(f"Kunne ikke åbne port: {e}", flush=True)
    exit(1)

# Definition af de mest sandsynlige test-scenarier ud fra dit dokument
test_id_liste = [1, 2, 9]  # De mest brugte Slave ID'er på disse print
test_adresser = [40, 177, 1, 100]  # LP C, LP, og klassiske startadresser
funktionskoder = [3, 4]  # 3 = Holding, 4 = Input

while True:
    for slave_id in test_id_liste:
        for func in funktionskoder:
            for adr in test_adresser:
                # Byg Modbus-pakke: ID (1 byte), Func (1 byte), Adresse (2 bytes), Antal (2 bytes: altid 00 01)
                pakke_data = bytes([slave_id, func]) + adr.to_bytes(2, byteorder='big') + bytes([0, 1])
                fuld_pakke = pakke_data + beregn_crc(pakke_data)
                
                print(f"[Scan] Prøver ID {slave_id} | Funktion 0{func} | Adresse {adr}...", flush=True)
                ser.write(fuld_pakke)
                time.sleep(0.15)
                
                if ser.in_waiting > 0:
                    svar = ser.read(ser.in_waiting)
                    hex_svar = " ".join(f"{b:02X}" for b in svar)
                    print(f"💥 HURRA! Svar modtaget fra VP: {hex_svar} !!!", flush=True)
                    print(f"-> Det virker med ID {slave_id}, Funktion 0{func}, Adresse {adr}", flush=True)
                    while True: time.sleep(1) # Stop scanningen, vi fandt det!
                    
    print("Scanning færdig uden svar. Starter forfra om 5 sekunder...", flush=True)
    time.sleep(5)
