FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y sqlite3

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Inicializa la base de datos antes de exponer el puerto y ejecutar la aplicación
RUN python -c 'from app import inicializar_db; inicializar_db()'

EXPOSE 80
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
