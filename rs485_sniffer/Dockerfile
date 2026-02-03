ARG BUILD_FROM
FROM ${BUILD_FROM}

# Sæt arbejdsmappe
WORKDIR /app

# Installer Python-pakker vi skal bruge
RUN apk add --no-cache \
    py3-pyserial \
    py3-paho-mqtt

# Kopiér filer ind i containeren
COPY run.sh /run.sh
COPY sniff_to_mqtt.py /app/sniff_to_mqtt.py

# Gør run.sh eksekverbar
RUN chmod +x /run.sh

# Start scriptet
CMD ["/run.sh"]
