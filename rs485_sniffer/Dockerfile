ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install Python + pip + required libs
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-serial \
    py3-paho-mqtt

WORKDIR /app

COPY sniff_to_mqtt.py /app/sniff_to_mqtt.py
COPY run.sh /run.sh

RUN chmod +x /run.sh

CMD ["/run.sh"]
