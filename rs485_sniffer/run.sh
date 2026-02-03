#!/usr/bin/with-contenv bash
set -e

echo "[rs485_sniffer] service started"
exec python3 /app/sniff_to_mqtt.py
