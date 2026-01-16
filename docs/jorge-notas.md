# Notas de trabajo - Jorge (2026-01-16)

## Objetivo
- Levantar SRNI en local replicando el entorno real con Docker.
- Trabajar aislado en `feature/jorge-setup` sin tocar `main`.
- Usar base de datos local con dump real para validar Backend + Frontend con datos.

## Control de versiones (Git)
- Repo clonado desde `main`.
- Rama creada para trabajo: `feature/jorge-setup`.
- Rama publicada en remoto y lista para PR cuando se requiera.

## Infraestructura (Docker - `infra/`)
- Servicios levantados con `docker compose up -d`:
  - PostgreSQL 16 (`postgres_local`)
  - MongoDB (`mongo_local`)
  - MinIO (`minio_local`)
  - Elasticsearch (`elastic_local`)
  - Kibana (`kibana_local`)
- Red Docker requerida por el stack:
  - `data_stack_net` (external)


## Base de datos (PostgreSQL local)
- Se restauró dump:
  - `srni_contratistas_dump_2026_01_16.sql`
- DB local usada:
  - DB_NAME: `contratistas`
  - DB_USER: `admin`
  - DB_HOST: `postgres_local`
- Validación en PostgreSQL:
  - Tablas presentes (ejemplos): `colaborador_core`, `dependencias`, `procedimiento`, `contrato_core`, etc.
  - Conteo validado:
    - `colaborador_core` = 92 registros
- Problema inicial y solución:
  - Error: `relation "colaborador_core" does not exist`
  - Solución: restauración del dump en PostgreSQL local.

## Backend (Django - `backend/rni_web/`)
- Backend levantado con Docker:
  - Contenedor: `rni_web`
  - URL: `http://localhost:8000`
- Variables de entorno usadas:
  - `.env` con credenciales de la BD local.
- Estado:
  - API responde correctamente con datos del dump.
- Prueba validada:
  - `GET http://localhost:8000/api/colaboradores/` retorna resultados.

## Frontend (Vite + React - `frontend/rni_front/`)
- Observación:
  - Dockerfile y docker-compose del frontend están vacíos (placeholders).
  - El frontend se levanta actualmente **sin Docker** (modo dev).
- Frontend levantado en local:
  - `npm install`
  - `npm run dev`
  - URL: `http://localhost:5173`
- Resultado:
  - Renderiza lista de colaboradores consumiendo el backend local.

## Decisiones tomadas
- No se modificaron modelos ni migraciones para evitar impactos y conflictos con `main`.
- Se trabajó con PostgreSQL local + dump para reproducibilidad y cero riesgo sobre la base principal.
- Se validó funcionamiento end-to-end (API + UI dev) en entorno local.

## Estado final
- Infra (`infra/`) arriba y estable.
- PostgreSQL local con datos reales restaurados.
- Backend disponible y respondiendo.
- Frontend dev disponible y consumiendo API.
- Trabajo listo para continuar desarrollo en `feature/jorge-setup` y luego PR cuando aplique.

------------------------------------------------------------------------------------------------

