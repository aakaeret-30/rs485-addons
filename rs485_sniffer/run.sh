#!/usr/bin/env bash
set -e

echo "[rs485_sniffer] starting sniff_to_mqtt.py"

exec python3 /sniff_to_mqtt.py
