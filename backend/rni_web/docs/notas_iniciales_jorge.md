# Notas de trabajo – Jorge

## Objetivo
Levantar el proyecto SRNI en entorno local de forma controlada, replicando el entorno real mediante Docker, sin afectar ramas principales ni bases de datos productivas, y dejando el entorno listo para desarrollo continuo.

---

## Rama de trabajo
- Rama utilizada: `feature/jorge-setup`
- Base tomada: `integration/django-templates`
- No se trabaja directamente sobre `main`.

---

## Backend – Estado actual

### Proyecto
- Backend basado en **Django**.
- Proyecto activo: `backend/rediapp`.

### Dockerización local
- Se creó configuración local con:
  - `Dockerfile`
  - `docker-compose.yml`
- Servicio expuesto en:
  - http://localhost:8010

### Base de datos
- PostgreSQL levantado vía Docker (`postgres_local`).
- Conexión por variables de entorno:
  - `DB_NAME`
  - `DB_USER`
  - `DB_PASSWORD`
  - `DB_HOST`
  - `DB_PORT`

> Importante: dentro de Docker **NO se usa `localhost`**, se usa el nombre del servicio (`postgres_local`).

---

## Configuración crítica aplicada

### settings.py
- Se adaptó `DATABASES` para usar variables de entorno.
- Se mantuvo compatibilidad con Docker y entorno local.
- Se respetaron templates, static y media según la rama integration.

---

## Estado funcional
- Backend levanta correctamente en Docker.
- Login funcional:
  - http://localhost:8010/login/
- Dashboard y vistas accesibles tras autenticación.
- Entorno estable para desarrollo.

---

## Flujo de trabajo acordado
- Desarrollo continuo en `feature/jorge-setup`.
- Revisión por Daniel.
- Aprobación y merge posterior a rama superior (según defina el equipo).

---

## Estado final
✔ Entorno local operativo  
✔ Docker funcional  
✔ Base de datos conectada  
✔ Listo para desarrollar sin riesgo  

Fecha: 2026-01-17
Autor: Jorge
