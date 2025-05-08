# Imagen base
FROM python:3.10-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 5003

# Comando para iniciar el microservicio
CMD ["python", "app.py"]
