# 📘 Contrato de API – RNI

Base URL (dev): http://localhost:8000

## Autenticación
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/auth/me/

## SQL controlado
POST /api/sql/execute/

## Dashboard
GET /api/dashboard/kpis/
GET /api/dashboard/colaboradores-por-equipo/
GET /api/dashboard/tipo-vinculacion/
GET /api/dashboard/actividades-por-frecuencia/
GET /api/dashboard/contratos-por-vigencia/

## Catálogos
GET /api/catalogos/equipos/
GET /api/catalogos/procedimientos/
