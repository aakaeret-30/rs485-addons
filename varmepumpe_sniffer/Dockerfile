ARG BUILD_FROM
FROM $BUILD_FROM

# Installer nødvendige Python-pakker
RUN apk add --no-cache python3 py3-pip \
    && pip3 install --no-cache-dir pyserial paho-mqtt --break-system-packages

# Kopier scriptet over i containeren
COPY sniff_to_mqtt.py /sniff_to_mqtt.py

# Kør scriptet ved opstart
CMD [ "python3", "/sniff_to_mqtt.py" ]
