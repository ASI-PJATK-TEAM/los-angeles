# Etap 1: Bazowy obraz
FROM python:3.12-slim

# Etap 2: Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    build-essential \
    gdal-bin \
    libgdal-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Ustaw zmienne środowiskowe (dla geopandas)
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV ENV="prod"

# Etap 3: Ustaw katalog roboczy
WORKDIR /app

# Etap 4: Kopiuj wymagania i zainstaluj je
COPY requirements-prod.txt .
RUN pip install --upgrade pip && pip install -r requirements-prod.txt

# Etap 5: Kopiuj cały projekt
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY kedro/data/06_models/crime_model ./model/

# Etap 6: Ustaw porty
EXPOSE 8000 8501

# Etap 7: Uruchom backend i frontend jednocześnie
CMD bash -c "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/main.py --server.port 8501"
