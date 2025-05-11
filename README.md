# README - Despliegue de la Aplicación BookStore en AWS usando Docker Swarm

## 🔖 1. Configuraciones Iniciales en los Microservicios

Para conectarse a una base de datos RDS en lugar de un contenedor MySQL local, debes modificar:

* En cada microservicio (`auth-service`, `catalog-service`, `transaction-service`) dentro de `config.py`:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<usuario>:<contraseña>@<endpoint-RDS>:<puerto>/<nombre-base-de-datos>'
```

**Notas:**

* `<usuario>`: usuario de tu instancia RDS.
* `<contraseña>`: contraseña de tu instancia RDS.
* `<endpoint-RDS>`: URL del RDS (por ejemplo: `bookstore-rds.cfj9xkz1ut5z.us-east-1.rds.amazonaws.com`).
* `<puerto>`: usualmente `3306`.
* `<nombre-base-de-datos>`: nombre de la base de datos.

No es necesario cambiar los `docker-compose.yml` locales si ya no vas a correr MySQL como contenedor.

---

## 🚀 2. Creación y Actualización de Imágenes Docker

Cada vez que hagas un cambio en el código fuente debes:

1. **Reconstruir la imagen** localmente:

```bash
docker build -t sebastianjimenez30/<nombre-servicio>:latest .
```

Por ejemplo, para `auth-service`:

```bash
docker build -t sebastianjimenez30/auth-service:latest .
```

2. **Loguearte a Docker Hub** (si no lo estás):

```bash
docker login
```

3. **Subir la nueva imagen**:

```bash
docker push sebastianjimenez30/<nombre-servicio>:latest
```

Repite esto para `auth-service`, `catalog-service`, `transaction-service` y `api-gateway`.

subes construyes y subes las imagenes de cada micro servicio como se indico al principio en estas rutas:

cd Microsevices/auth-service
cd Microsevices/catalog-service
cd Microsevices/transaction-service
cd Microsevices/api\_gateway

**IMPORTANTE:** Cada vez que hagas cambios en el código debes volver a construir y subir las nuevas imágenes. los ejemplos son con mi usuario pero podrias utilizar tu usuario de dockerhub

---

## 🌐 3. Creación de Instancias en AWS

Debes crear 4 instancias EC2:

| Rol      | Tamaño sugerido   | Sistema Operativo |
| -------- | ----------------- | ----------------- |
| Manager  | t2.medium o mejor | Ubuntu 22.04      |
| Worker 1 | t2.medium o mejor | Ubuntu 22.04      |
| Worker 2 | t2.medium o mejor | Ubuntu 22.04      |
| Worker 3 | t2.medium o mejor | Ubuntu 22.04      |

**Recomendaciones:**

* Asignar al menos 2 vCPUs y 4 GB de RAM para cada instancia.
* Asignar IP Pública y permitir conexión SSH (puerto 22).

**Reglas de entrada (Security Group) necesarias:**

| Tipo         | Protocolo | Puerto    | Origen    |
| ------------ | --------- | --------- | --------- |
| SSH          | TCP       | 22        | Tu IP     |
| HTTP         | TCP       | 80        | 0.0.0.0/0 |
| HTTPS        | TCP       | 443       | 0.0.0.0/0 |
| Docker Swarm | TCP/UDP   | 2377      | 0.0.0.0/0 |
| Docker Swarm | TCP/UDP   | 7946      | 0.0.0.0/0 |
| Docker Swarm | UDP       | 4789      | 0.0.0.0/0 |
| App Ports    | TCP       | 5000-5003 | 0.0.0.0/0 |

---

## 🚄 4. Conectarse a las Instancias

Desde tu máquina local:

```bash
ssh -i <tu-llave.pem> ubuntu@<IP-pública>
```

Haz esto para el **Manager** y cada **Worker**.

---

## 🔧 5. Ejecución de los Scripts

Los scripts se encuentran en:
[https://github.com/camazog1/BookStore.git](https://github.com/camazog1/BookStore.git) rama `BookStoreMicroservices`

### En el Manager

Clonas el repositorio:

```bash
git clone -b BookStoreMicroservices https://github.com/camazog1/BookStore.git
cd BookStore
```



Y ejecutas:

```bash
chmod +x manager-setup.sh deploy-services.sh auto-scale.sh
./manager-setup.sh
./deploy-services.sh
```

**manager-setup.sh**:

* Inicializa Docker Swarm.
* Crea la red `bookstore_net_swarm`.

**deploy-services.sh**:

* Despliega todos los servicios.

### En cada Worker

Clonas el repositorio:

```bash
git clone -b BookStoreMicroservices https://github.com/camazog1/BookStore.git
cd BookStore
```

**IMPORTANTE:** Antes de ejecutar `workerX-setup.sh`, debes modificar la línea del `workerX-setup.sh` para poner el token correcto que obtuviste al inicializar el swarm.

Ejecutas:

```bash
chmod +x worker1-setup.sh
./worker1-setup.sh
```

Repites igual para `worker2-setup.sh` y `worker3-setup.sh`.

---

## 🔄 6. Para Auto-Escalar los Servicios

Desde el **Manager**, ejecutas:

```bash
./auto-scale.sh
```

Este script escala los servicios a más réplicas de acuerdo a la configuración.

---

## 🚫 Errores Comunes

* **Fallo de conexión a RDS:** Asegúrate de que el RDS permita acceso público (o al menos desde las IPs de tus instancias).
* **Error de token en Workers:** Recuerda actualizar el `join-token` si inicializas de nuevo el manager.
* **Puerto en uso:** Verifica que los puertos 5000-5003 estén libres.

