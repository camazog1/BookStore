# Proyecto 2 – Aplicación Escalable: BookStore

**Universidad EAFIT – ST0263: Tópicos Especiales en Telemática, 2025-1**  
**Fecha de entrega:** 12 de mayo de 2025

---

## 🧾 Descripción general

BookStore es una aplicación monolítica desarrollada en Flask que simula un sistema de ecommerce de libros de segunda mano, donde los usuarios pueden autenticarse, publicar, comprar, pagar y simular la entrega de libros. Este proyecto consiste en desplegar la aplicación de forma escalable en la nube (AWS), siguiendo tres objetivos específicos.

---

## ✅ Objetivo 1 – Despliegue de la aplicación monolítica en una VM (20%)

- Se utilizó una instancia EC2 en AWS (Ubuntu 22.04).
- Se desplegó la aplicación BookStore monolítica usando Docker y Docker Compose.
- Se configuró NGINX como proxy inverso.

---

## ✅ Objetivo 2 – Escalamiento monolítico con infraestructura en la nube (30%)

- Se creó una imagen AMI de la instancia BookStore original.
- Se implementó un Auto Scaling Group con al menos dos instancias EC2.
- Se utilizó un Load Balancer (ELB) administrado de AWS para balancear tráfico HTTP/HTTPS.
- Se migró la base de datos a Amazon RDS (MySQL 8).
- Se configuró almacenamiento compartido mediante Amazon EFS (NFS) y se montó en las instancias EC2.
- El sistema es tolerante a fallos y escalable horizontalmente.

---

## 📦 Tecnologías utilizadas

- Python 3 + Flask
- Docker + Docker Compose
- NGINX
- AWS EC2, RDS, ELB, EFS
- Certbot + Let's Encrypt
- GitHub

---

## 🔀 Objetivo 3 – Microservicios (50%)

Para el desarrollo del Objetivo 3, que consiste en dividir la aplicación en microservicios (`auth`, `catalog`, `transaction`):

👉 [`BookStoreMicroservices`](https://https://github.com/camazog1/BookStore/treeBookStoreMicroservices)

---

## 👥 Autores

- Carlos Mazo  
- Anderson Jimenez
