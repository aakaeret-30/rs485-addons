ARG BUILD_FROM
FROM $BUILD_FROM

# Kopiér add-on filer
COPY run.sh /run.sh
COPY sniff_to_mqtt.py /sniff_to_mqtt.py

RUN chmod +x /run.sh

# s6 service definition
RUN mkdir -p /etc/services.d/rs485_sniffer
COPY service_run /etc/services.d/rs485_sniffer/run
RUN chmod +x /etc/services.d/rs485_sniffer/run
