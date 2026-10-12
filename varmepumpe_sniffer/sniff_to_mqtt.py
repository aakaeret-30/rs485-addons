import serial
import paho.mqtt.client as mqtt
import time
import binascii
import sys

# --- KONFIGURATION FOR VARMEPUMPE ---
SERIAL_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AU0YA7RI-if00-port0"
BAUDRATE = 9600
MQTT_BROKER = "core-mosquitto"
MQTT_TOPIC_RAW = "valdemar/vp/raw"

print("Starter Valdemar VP scanner...", flush=True)

# Opsætning av MQTT
mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
    print("MQTT Forbundet succesfuldt.", flush=True)
except Exception as e:
    print(f"MQTT fejl: {e}", flush=True)

# Åbn porten til BÅDE at læse og skrive
print(f"Åbner seriel port i SCANNER-mode: {SERIAL_PORT}", flush=True)
try:
    ser = serial.Serial(
        port=SERIAL_PORT, baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE, timeout=1.0
    )
    print("Seriel port åbnet uden fejl.", flush=True)
except Exception as e:
    print(f"Kunne ikke åbne port: {e}", flush=True)
    exit(1)

# En standard Modbus-forespørgsel (Læs Holding Register 40 / LP C)
query_lpc = b'\x01\x03\x00\x28\x00\x01\x85\xC3'

while True:
    print("Sender forespørgsel efter LP C (Adresse 40)...", flush=True)
    try:
        ser.write(query_lpc)
    except Exception as e:
        print(f"Fejl ved afsendelse på ledning: {e}", flush=True)
    
    # Vent kortvarigt på svar fra varmepumpen
    time.sleep(0.5)
    
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting)
        hex_string = binascii.hexlify(response).decode('utf-8').upper()
        formatted_hex = " ".join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
        print(f"RÅT SVAR FRA VP: {formatted_hex}", flush=True)
        mqtt_client.publish(MQTT_TOPIC_RAW, formatted_hex)
    else:
        print("Intet svar modtaget fra varmepumpen (Timeout).", flush=True)
        
    time.sleep(4.5)
