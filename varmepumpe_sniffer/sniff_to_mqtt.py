import serial
import paho.mqtt.client as mqtt
import time
import binascii

# --- KONFIGURATION FOR VARMEPUMPE ---
SERIAL_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AU0YA7RI-if00-port0"
BAUDRATE = 9600
MQTT_BROKER = "core-mosquitto"
MQTT_TOPIC_RAW = "valdemar/vp/raw"

# Opsætning af MQTT
mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(MQTT_BROKER, 1883, 60)
    mqtt_client.loop_start()
except Exception as e:
    print(f"MQTT fejl: {e}")

# Åbn porten til BÅDE at læse og skrive
print(f"Åbner seriel port i SCANNER-mode: {SERIAL_PORT}")
try:
    ser = serial.Serial(
        port=SERIAL_PORT, baudrate=BAUDRATE,
        bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE, timeout=1.0
    )
except Exception as e:
    print(f"Kunne ikke åbne port: {e}")
    exit(1)

# En standard Modbus-forespørgsel (Læs Holding Register 40 / LP C)
# hex: 01 (Slave ID) 03 (Læs) 00 28 (Adresse 40) 00 01 (Læs 1 register) 85 C3 (CRC Tjeksum)
query_lpc = b'\x01\x03\x00\x28\x00\x01\x85\xC3'

while True:
    print("Sender forespørgsel efter LP C (Adresse 40)...")
    try:
        ser.write(query_lpc)
    except Exception as e:
        print(f"Fejl ved afsendelse: {e}")
    
    # Vent kortvarigt på svar fra varmepumpen
    time.sleep(0.5)
    
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting)
        hex_string = binascii.hexlify(response).decode('utf-8').upper()
        formatted_hex = " ".join(hex_string[i:i+2] for i in range(0, len(hex_string), 2))
        print(f"RÅT SVAR FRA VP: {formatted_hex}")
        mqtt_client.publish(MQTT_TOPIC_RAW, formatted_hex)
    else:
        print("Intet svar modtaget fra varmepumpen (Timeout). Prøver om 5 sekunder...")
        
    time.sleep(4.5)
