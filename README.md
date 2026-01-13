# SRNI Platform

Plataforma institucional para **gestión de información contractual y documental**, basada en una arquitectura moderna, desacoplada y reproducible mediante contenedores Docker.

---

## 🎯 Objetivo

Centralizar la información de **colaboradores, contratos y documentos**, reemplazando procesos manuales basados en archivos dispersos (Excel), y habilitando:

* trazabilidad,
* control documental,
* búsqueda avanzada,
* base sólida para automatización y analítica.

---

## 🧱 Arquitectura general

La plataforma está organizada por **capas claramente separadas**:

```text
infra/      → Stack de datos (PostgreSQL, MongoDB, MinIO, Elasticsearch, Kibana)
backend/    → API institucional (Django + Django REST Framework)
frontend/   → Aplicación web (React + Vite)
scripts/    → Inicialización reproducible (Mongo, MinIO, Elasticsearch)
compose/    → Orquestación completa del sistema
docs/       → Informes técnicos y diagramas
```

Todo el sistema es **Docker-first**, portable a servidor, CI/CD o Kubernetes.

---

## ⚙️ Componentes principales

| Componente    | Rol                                            |
| ------------- | ---------------------------------------------- |
| PostgreSQL    | Datos estructurados (colaboradores, contratos) |
| MongoDB       | Metadatos documentales y relaciones flexibles  |
| MinIO         | Almacenamiento de documentos (object storage)  |
| Elasticsearch | Indexación y búsqueda                          |
| Kibana        | Exploración analítica                          |
| Django REST   | Exposición de API institucional                |
| React         | Interfaz web institucional                     |

---

## 🚀 Despliegue rápido

### 1️⃣ Infraestructura de datos

```bash
cd infra
docker compose up -d
```

---

### 2️⃣ Backend (API)

```bash
cd backend/rni_web
docker compose up -d
```

API disponible en:

```
http://localhost:8000
```

---

### 3️⃣ Frontend

```bash
cd frontend/rni_front
docker compose up -d
```

Aplicación web disponible en:

```
http://localhost:5173
```

---

### 4️⃣ Sistema completo (opcional)

```bash
cd compose
docker compose -f docker-compose.full.yml up -d
```

Levanta **infraestructura + backend + frontend** en una sola ejecución.

---

## 🧪 Validación básica

### API (terminal)

```bash
curl http://localhost:8000/api/colaboradores/
```

---

### MongoDB

```bash
mongosh mongodb://localhost:27017
use gestion_documental
show collections
```

---

### MinIO

Consola web:

```
http://localhost:9001
```

---

### Kibana

```
http://localhost:5601
```

---

## 📦 Persistencia de datos

Los datos se almacenan en **volúmenes externos a Git**:

```text
infra/*/data/
```

Esto garantiza:

* seguridad,
* durabilidad,
* limpieza del repositorio.

---

## 📜 Scripts de inicialización

Los scripts en `scripts/` permiten crear la infraestructura **sin pasos manuales**:

* MongoDB: colecciones e índices
* MinIO: buckets, versionado y lifecycle
* Elasticsearch: índices y mappings

Esto habilita trazabilidad, auditoría y despliegue automatizado.

---

## 🧭 Estado actual

* ✅ Infraestructura operativa
* ✅ API funcional
* ✅ Frontend conectado
* ✅ Normalización en MongoDB
* 🚧 Indexación avanzada y dashboards (en progreso)

---

## 📌 Próximos pasos

* Indexación documental avanzada en Elasticsearch
* Dashboards institucionales
* Autenticación y control de acceso
* Preparación para CI/CD y Kubernetes

---

## 👤 Responsable técnico

**Daniel Campos**
Arquitectura de datos · Backend · Automatización

---
