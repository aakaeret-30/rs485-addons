ARG BUILD_FROM
FROM ${BUILD_FROM}

WORKDIR /app

RUN pip install --no-cache-dir pyserial paho-mqtt

COPY sniff_to_mqtt.py /app/sniff_to_mqtt.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
