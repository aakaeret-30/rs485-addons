FROM ghcr.io/home-assistant/aarch64-base:latest

# Installer nødvendige Python-pakker via apk (IKKE pip)
RUN apk add --no-cache \
    python3 \
    py3-serial \
    py3-paho-mqtt

# Arbejdsmappe
WORKDIR /app

# Kopiér applikationsfiler
COPY run.sh sniff_to_mqtt.py /app/

# Sørg for at run.sh er eksekverbar
RUN chmod +x /app/run.sh

# Startpunkt (PID 1, ingen s6)
CMD ["/app/run.sh"]
