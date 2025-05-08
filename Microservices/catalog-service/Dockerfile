# Imagen base oficial
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del servicio
EXPOSE 5002

# Comando para ejecutar el microservicio
CMD ["python", "app.py"]
