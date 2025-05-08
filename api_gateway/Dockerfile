# Imagen base
FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar el contenido del gateway
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "app.py"]
