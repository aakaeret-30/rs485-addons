#!/usr/bin/with-contenv bash
set -e

echo "[rs485_sniffer] Starting RS485 sniffer..."
python3 /app/sniff_to_mqtt.py
