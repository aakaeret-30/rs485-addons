import serial
import paho.mqtt.client as mqtt
import time
import binascii

# --- KONFIGURATION FOR VARMEPUMPE ---
SERIAL_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AU0YA7RI-if00-port0"
BAUDRATE = 9600
MQTT_BROKER = "core-mosquitto"
MQTT_TOPIC_LP = "valdemar/vp/lp"
MQTT_TOPIC_LPC = "valdemar/vp/lpc"

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

# Opsætning af MQTT
mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
    print("MQTT Forbundet.", flush=True)
except Exception as e:
    print(f"MQTT fejl: {e}", flush=True)

print(f"Åbner port til produktion: {SERIAL_PORT}", flush=True)
try:
    ser = serial.Serial(
        port=SERIAL_PORT, baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE, timeout=1.0
    )
except Exception as e:
    print(f"Kunne ikke åbne port: {e}", flush=True)
    exit(1)

# Generer anmodninger (Func 03) for de to rigtige live-adresser
# Adresse 95 (LP C) og Adresse 177 (LP)
req_lpc = bytes([1, 3]) + int(95).to_bytes(2, byteorder='big') + bytes([0, 1])
req_lpc += beregn_crc(req_lpc)

req_lp = bytes([1, 3]) + int(177).to_bytes(2, byteorder='big') + bytes([0, 1])
req_lp += beregn_crc(req_lp)

while True:
    # 1. Hent LP C (Adresse 95)
    ser.write(req_lpc)
    time.sleep(0.3)
    if ser.in_waiting > 0:
        res = ser.read(ser.in_waiting)
        if len(res) >= 5 and res[1] == 3:
            val = int.from_bytes(res[3:5], byteorder='big', signed=True)
            lpc_temp = val * 0.1
            print(f"[Live] LP C Temperatur: {lpc_temp} °C", flush=True)
            mqtt_client.publish(MQTT_TOPIC_LPC, str(lpc_temp))
            
    time.sleep(1.0)
    
    # 2. Hent LP (Adresse 177)
    ser.write(req_lp)
    time.sleep(0.3)
    if ser.in_waiting > 0:
        res = ser.read(ser.in_waiting)
        if len(res) >= 5 and res[1] == 3:
            val = int.from_bytes(res[3:5], byteorder='big', signed=True)
            lp_bar = val * 0.1
            print(f"[Live] LP Tryk: {lp_bar} bar", flush=True)
            mqtt_client.publish(MQTT_TOPIC_LP, str(lp_bar))

    time.sleep(3.4)
