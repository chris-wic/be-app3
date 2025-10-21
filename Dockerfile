FROM tiangolo/uvicorn-gunicorn:python3.11-slim

# Certificati CA per TLS
USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copiamo app che contiene main.py
COPY ./src /src
COPY ./main.py main.py

# Copiamo il file con le librerie da installare
COPY requirements.txt /src/requirements.txt

# Filtriamo requirements rimuovendo commenti (inizio e in coda) e righe vuote. Poi installiamo le librerie.
RUN sed 's/#.*$//' /src/requirements.txt | sed '/^\s*$/d' > /tmp/req.txt \
    && pip install --no-cache-dir -r /tmp/req.txt