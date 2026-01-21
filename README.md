# SRNI Platform

Plataforma institucional para la **gestión de información contractual, documental y analítica**, basada en una arquitectura moderna, desacoplada y reproducible mediante contenedores Docker.

El sistema está diseñado para soportar procesos internos de la **Red Nacional de Información (RNI)**, con énfasis en trazabilidad, control documental, interoperabilidad y analítica.

---

## 🎯 Objetivo

Centralizar la información de **colaboradores, contratos, documentos y proyectos tecnológicos**, reemplazando procesos manuales basados en archivos dispersos (Excel), y habilitando:

- Trazabilidad institucional
- Control documental y versionado
- Búsqueda avanzada e indexación
- Base sólida para automatización, analítica y dashboards

---

## 🧱 Arquitectura general

La plataforma se organiza por **capas claramente separadas**, siguiendo principios de arquitectura limpia y desacoplamiento:

```text
infra/      → Stack de datos (PostgreSQL, MongoDB, MinIO, Elasticsearch, Kibana)
backend/    → API institucional (Django + Django REST Framework)
frontend/   → Aplicación web (React + Vite)
scripts/    → Inicialización reproducible de servicios
compose/    → Orquestación completa del sistema
docs/       → Documentación técnica y arquitectónica
````

Todo el sistema es **Docker-first**, portable a servidores locales, CI/CD o entornos orquestados (Kubernetes).

---

## ⚙️ Componentes principales

| Componente    | Rol principal                                       |
| ------------- | --------------------------------------------------- |
| PostgreSQL    | Datos estructurados (contratos, personas, procesos) |
| MongoDB       | Metadatos flexibles y snapshots                     |
| MinIO         | Almacenamiento documental (object storage)          |
| Elasticsearch | Indexación y búsqueda                               |
| Kibana        | Exploración analítica                               |
| Django REST   | API institucional                                   |
| React + Vite  | Interfaz web institucional                          |

---

## 🧩 Módulos destacados

### 📊 Módulo SINAPSIS

Dashboard analítico para la visualización del **portafolio de proyectos tecnológicos**, integrando información externa y normalizada.

📄 Documentación técnica detallada:

* [`docs/sinapsis/dashboard_sinapsis.md`](docs/sinapsis/dashboard_sinapsis.md)

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

### API

```bash
curl http://localhost:8000/api/colaboradores/
```

### MongoDB

```bash
mongosh mongodb://localhost:27017
use gestion_documental
show collections
```

### MinIO

```
http://localhost:9001
```

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

Esto garantiza seguridad, durabilidad y limpieza del repositorio.

---

## 📜 Scripts de inicialización

El directorio `scripts/` contiene rutinas reproducibles para:

* Inicialización de MongoDB (colecciones, índices)
* Configuración de buckets y versionado en MinIO
* Creación de índices en Elasticsearch

Estos scripts eliminan pasos manuales y habilitan despliegue automatizado.

---

## 🧭 Estado actual

* ✅ Infraestructura operativa
* ✅ API funcional
* ✅ Frontend conectado
* ✅ Integración SINAPSIS
* 🚧 Indexación avanzada y autenticación (en progreso)

---

## 📌 Próximos pasos

* Dashboards analíticos avanzados
* Autenticación y control de acceso
* Preparación para CI/CD y Kubernetes
* Documentación académica y técnica extendida

---

## 👤 Responsable técnico

**Daniel Campos**
Arquitectura de datos · Backend · Automatización