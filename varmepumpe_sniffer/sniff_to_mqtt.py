import serial
import paho.mqtt.client as mqtt
import time
import binascii

# --- KONFIGURATION FOR VARMEPUMPE ---
SERIAL_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AU0YA7RI-if00-port0"
BAUDRATE = 9600
MQTT_BROKER = "core-mosquitto"  # Standard navn for HA Mosquitto broker
MQTT_TOPIC_RAW = "valdemar/vp/raw"

def on_connect(client, userdata, flags, rc):
    print(f"Forbundet til MQTT med resultatkode {rc}")

# Opsætning af MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect

try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
except Exception as e:
    print(f"Kunne ikke forbinde til MQTT: {e}")

# Åbn den serielle port som ren lytter
print(f"Åbner seriel port: {SERIAL_PORT}")
try:
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.1
    )
except Exception as e:
    print(f"Kunne ikke åbne seriel port: {e}")
    exit(1)

buffer = bytearray()

while True:
    if ser.in_waiting > 0:
        raw_data = ser.read(ser.in_waiting)
        buffer.extend(raw_data)
        
        # Hvis der er en pause i dataene, antager vi at pakken er færdig
        time.sleep(0.05)
        if ser.in_waiting == 0:
            hex_string = binascii.hexlify(buffer).decode('utf-8').upper()
            # Del op i læsbare bytes: "01 03 00 28 ..."
            formatted_hex = " ".join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
            
            print(f"Opsnappet pakke: {formatted_hex}")
            mqtt_client.publish(MQTT_TOPIC_RAW, formatted_hex)
            
            buffer.clear()
    else:
        time.sleep(0.01)
