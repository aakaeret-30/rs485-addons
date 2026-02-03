FROM ghcr.io/home-assistant/aarch64-base:latest

# Installer Python + nødvendige libs via apk (ingen pip)
RUN apk add --no-cache \
    python3 \
    py3-pyserial \
    py3-paho-mqtt

WORKDIR /app

COPY run.sh sniff_to_mqtt.py /app/

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
