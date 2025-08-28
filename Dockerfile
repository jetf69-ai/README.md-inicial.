# Usa Python 3.11 oficial
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt .
COPY app.py .
COPY vehicles_us.csv .
COPY README.md .

# Instala dependencias
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Expone el puerto que Streamlit usará
EXPOSE 8501

# Comando para iniciar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
