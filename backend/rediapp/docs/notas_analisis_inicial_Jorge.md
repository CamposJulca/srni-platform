# Registro de revisión técnica – Jorge (RedIapp / SRNI)

## Contexto
- Rama base para trabajo: `integration/django-templates`se toma y se trabaja en Features
- Objetivo: Validar backend Django (RedIapp) y dejarlo reproducible en local vía Docker + dump, sin depender del servidor/ngrok.

## Estado actual observado
- Existen dos backends en el repo:
  - `backend/rni_web` (API DRF)
  - `backend/rediapp` (Django templates + módulos: accounts, dashboard, colaboradores, automatización, etc.)
- El dump está cargado en `postgres_local` con BD `contratistas`.


## Correcciones mínimas aplicadas / sugeridas
- Consolidar el modelo `ColaboradorCore` únicamente en `apps/colaboradores/models.py` con:
  - `managed = False`
  - `db_table = "colaborador_core"`
- Definir vista `list_colaboradores` que consulte `ColaboradorCore` y renderice template.
- Ajustar `apps/colaboradores/urls.py` con:
  - `app_name = "colaboradores"`
  - ruta `path("", ..., name="list")`

## Recomendación de consolidación (limpieza de arquitectura)
- Tomar `backend/rediapp` como backend principal de UI (templates).
- Migrar gradualmente la lógica que hoy vive en `rni_web` (modelos/tablas SRNI) hacia `rediapp/apps/*` usando modelos `managed=False`.
- Mantener `rni_web` como referencia o API separada hasta completar migración.
- Unificar acceso a BD por `.env` (evitar credenciales hardcodeadas como `HOST=localhost` dentro del contenedor).

## Próximos pasos sugeridos
- correccion de cierre de cesion funcional que rediriga nuevamente a Login
- Terminar módulo Colaboradores: listar, detalle, filtros básicos, organizandolo todo en rediapp.
- Validar Dashboard + Automatización Documental contra BD local.
- Luego definir estrategia de frontend (si se mantiene templates o si se migra a React) de forma incremental, sin bloquear operación actual.
