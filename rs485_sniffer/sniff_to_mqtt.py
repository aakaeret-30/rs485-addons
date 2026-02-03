# [INDRYK = 0]
import serial
import time
import struct
import paho.mqtt.client as mqtt

SERIAL_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AW6CH20W-if00-port0"
BAUDRATE = 9600

MQTT_HOST = "core-mosquitto"
MQTT_PORT = 1883
MQTT_USER = "rs485"
MQTT_PASS = "rs485test"

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)

while True:
    try:
        print("[mqtt] Connecting to broker...")
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        print("[mqtt] Connected")
        break
    except Exception as e:
        print(f"[mqtt] Not ready yet: {e}")
        time.sleep(5)

client.loop_start()

while True:
    try:
        print(f"[serial] Opening {SERIAL_PORT}")
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUDRATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.2,
        )
        print("[serial] Opened")
        break
    except Exception as e:
        print(f"[serial] Not ready yet: {e}")
        time.sleep(5)

buffer = bytearray()


# [INDRYK = 0]
while True:

    # [INDRYK = 4]
    data = ser.read(256)

    # [INDRYK = 4]
    if data:

        # [INDRYK = 8]
        buffer.extend(data)
        time.sleep(0.05)
        buffer.extend(ser.read(256))

        # [INDRYK = 8]
        for i in range(len(buffer) - 16):

            # [INDRYK = 12]
            if buffer[i] != 0x04:
                continue

            if buffer[i + 1] != 0x03:
                continue

            raw_hex = buffer[i:i + 15].hex()
            client.publish("rs485/dtsu666/raw", raw_hex)

            if buffer[i + 2] != 0x0C:
                continue

            frame = buffer[i + 3:i + 15]

            # [INDRYK = 12]
            try:
                p_l1 = struct.unpack(">f", frame[0:4])[0]
                p_l2 = struct.unpack(">f", frame[4:8])[0]
                p_l3 = struct.unpack(">f", frame[8:12])[0]
            except struct.error:
                continue

            client.publish("rs485/dtsu666/p_l1", round(p_l1 / 10, 1))
            client.publish("rs485/dtsu666/p_l2", round(p_l2 / 10, 1))
            client.publish("rs485/dtsu666/p_l3", round(p_l3 / 10, 1))

            buffer.clear()
            break

    # [INDRYK = 4]
    else:
        time.sleep(0.05)


