# Imagen base oficial de Python
FROM python:3.10-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde correrá el servicio
EXPOSE 5001

# Comando para ejecutar el servicio Flask
CMD ["python", "app.py"]
