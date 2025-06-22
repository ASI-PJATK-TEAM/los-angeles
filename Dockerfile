FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gdal-bin \
    libgdal-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV ENV="prod"

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install --upgrade pip && pip install -r requirements-prod.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY kedro/data/06_models/crime_model ./model/

EXPOSE 8000 8501

CMD bash -c "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/main.py --server.port 8501"
