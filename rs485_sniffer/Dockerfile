ARG BUILD_FROM
FROM $BUILD_FROM

# Kopiér Python-script
COPY sniff_to_mqtt.py /sniff_to_mqtt.py

# Opret s6 service
RUN mkdir -p /etc/services.d/rs485_sniffer
COPY service_run /etc/services.d/rs485_sniffer/run
RUN chmod +x /etc/services.d/rs485_sniffer/run
