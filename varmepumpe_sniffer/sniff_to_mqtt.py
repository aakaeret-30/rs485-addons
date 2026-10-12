import serial
import paho.mqtt.client as mqtt
import time
import binascii

# --- KONFIGURATION FOR VARMEPUMPE (PASSIV SNIFFER) ---
SERIAL_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AU0YA7RI-if00-port0"
BAUDRATE = 9600
MQTT_BROKER = "core-mosquitto"
MQTT_TOPIC_RAW = "valdemar/vp/raw"

print("Starter passiv display-sniffer...", flush=True)

# Opsætning af MQTT
mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
    print("MQTT Forbundet.", flush=True)
except Exception as e:
    print(f"MQTT fejl: {e}", flush=True)

# Åbn den serielle port som REN passiv lytter
print(f"Åbner seriel port som LYTTER: {SERIAL_PORT}", flush=True)
try:
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.05
    )
    print("Seriel port åbnet. Venter på datatrafik fra displayet...", flush=True)
except Exception as e:
    print(f"Kunne ikke åbne port: {e}", flush=True)
    exit(1)

buffer = bytearray()

while True:
    if ser.in_waiting > 0:
        raw_data = ser.read(ser.in_waiting)
        buffer.extend(raw_data)
        
        # En lille pause for at sikre, at hele pakken er kommet med over linjen
        time.sleep(0.03)
        if ser.in_waiting == 0:
            hex_string = binascii.hexlify(buffer).decode('utf-8').upper()
            formatted_hex = " ".join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
            
            print(f"Opsnappet display-pakke: {formatted_hex}", flush=True)
            mqtt_client.publish(MQTT_TOPIC_RAW, formatted_hex)
            
            buffer.clear()
    else:
        time.sleep(0.01)
