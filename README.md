# Proyecto 2: Aplicación Escalable - Objetivo 3

## Descripción del Objetivo 3

En este objetivo, realizamos una reingeniería de la aplicación **BookStore Monolítica** para dividirla en **tres microservicios** independientes, los cuales son:

1. **Microservicio de Autenticación**: Gestiona el registro, inicio de sesión y cierre de sesión de los usuarios.
2. **Microservicio de Catálogo**: Permite visualizar la oferta de libros disponibles en la plataforma.
3. **Microservicio de Compra, Pago y Entrega**: Gestiona el proceso de compra de libros, simula el pago y el envío de los mismos.

### Desafíos con Kubernetes

Durante el desarrollo, intentamos utilizar **Kubernetes** para gestionar y orquestar los microservicios. Sin embargo, nos encontramos con dificultades técnicas y limitaciones que no nos permitieron completar la implementación de Kubernetes dentro del tiempo disponible. Debido a estos problemas, no pudimos desplegar la aplicación correctamente en un clúster de Kubernetes.

### Solución: Docker Swarm

Para poder entregar el proyecto a tiempo, decidimos optar por **Docker Swarm** como solución de orquestación de contenedores. Docker Swarm nos permitió desplegar los microservicios en un entorno de producción utilizando un enfoque más sencillo y accesible.

## Pasos Realizados

### 1. Reingeniería de la Aplicación Monolítica

La aplicación original de **BookStore** fue reestructurada para que sus funcionalidades se distribuyan en tres microservicios independientes. Cada microservicio se encargará de una función específica de la aplicación:

- **Microservicio de Autenticación**:
  - Se encargará de gestionar el registro, login y logout de los usuarios.
  - Fue implementado usando **Flask** para la API REST.

- **Microservicio de Catálogo**:
  - Proporciona las funcionalidades para visualizar la oferta de libros disponibles.
  - Este servicio también fue implementado con **Flask** y se conecta a la base de datos para acceder al catálogo de libros.

- **Microservicio de Compra, Pago y Entrega**:
  - Gestiona el proceso de compra de los libros, la simulación de pagos y la gestión del envío de libros.
  - Implementado con **Flask** para las API necesarias y con integración con servicios simulados para el pago y envío.

### 2. Despliegue con Docker Swarm

En lugar de Kubernetes, utilizamos **Docker Swarm** para orquestar los contenedores de los microservicios:

- **Creación de la pila de Docker Swarm**: Se creó un archivo `docker-compose.yml` para definir los servicios de los tres microservicios. Docker Swarm gestionó la orquestación de los contenedores en un clúster de Docker.
- **Escalabilidad en Docker Swarm**: Aunque Docker Swarm no proporciona la misma complejidad que Kubernetes, utilizamos sus capacidades para escalar los servicios de manera manual, ajustando el número de réplicas según fuera necesario.
- **Redes y Volúmenes**: Configuramos redes de contenedores y volúmenes compartidos para asegurar la comunicación entre los microservicios y el almacenamiento persistente.

### 3. Configuración de la Base de Datos y Archivos

- **Base de Datos**: La base de datos fue gestionada utilizando **Amazon RDS** con **MySQL** como motor de base de datos. Esto garantiza alta disponibilidad, backups automáticos y escalabilidad administrada por AWS. Los microservicios en Docker Swarm se conectan remotamente a esta base de datos.

### 4. Seguridad

- Se implementó el acceso seguro a la aplicación utilizando **SSL/TLS**, con el objetivo de encriptar las comunicaciones entre los clientes y los microservicios.
- Se compró un **dominio personalizado en Hostinger** y se configuró el certificado SSL correspondiente a través de AWS Certificate Manager.
- El dominio está correctamente apuntado a la infraestructura en AWS, y el certificado SSL fue validado con los registros CNAME.
- Sin embargo, **hasta el momento el acceso vía HTTPS no ha funcionado correctamente** por lo que este punto del certificado no lo consideramos completado.

## Arquitectura

La arquitectura implementada está compuesta por los siguientes componentes:

1. **Docker Swarm**: Para orquestar y gestionar los contenedores de los microservicios.
2. **MySQL en AWS**: Base de datos gestionada en Amazon RDS.
3. **Microservicios desplegados en Docker Swarm**: Cada microservicio se ejecuta en un contenedor dentro de un nodo en el clúster Docker Swarm.
4. **Balanceador de Carga**: Utilizamos un **reverse proxy NGINX** dentro de Docker Swarm para distribuir el tráfico entre los microservicios.