# Nota de Migración Inicial – Backend (Jorge)

## Contexto
Se realizó la migración inicial del backend según lo solicitado por Daniel, con el objetivo de consolidar el backend en un solo lugar funcional y validado, manteniendo la modularidad del proyecto.

Anteriormente, el sistema funcionaba como un monolito en Django con HTML templates. El objetivo actual es separar claramente:
- Backend: Django
- Frontend: React (fase posterior)

## Trabajo realizado

1. **Migración de backend**
   - Se trasladó la lógica funcional existente desde `rediapp` hacia `rni_web`.
   - Se replicó la misma información, modelos y funcionalidades en `rni_web`, tal como fue solicitado.
   - `rediapp` se mantiene únicamente como carpeta de respaldo (legacy), en caso de requerir consultar o trasladar información adicional.

2. **Validación funcional**
   - Se levantó el proyecto correctamente en entorno local usando Docker.
   - Se validó conexión con la base de datos mediante dump existente.
   - Se confirmó funcionamiento de:
     - Admin Django
     - Módulo de colaboradores
     - Dashboard (ajustado para usar ORM y respetar el esquema real del dump).

3. **Correcciones técnicas**
   - Se ajustaron consultas SQL frágiles a ORM para evitar dependencia de nombres físicos de tablas.
   - Se alinearon los modelos a las tablas reales del dump (`managed = False`).
   - Se corrigieron dependencias de red Docker (infraestructura y backend).

## Estado actual
- `rni_web` es el backend principal y funcional.
- El proyecto levanta correctamente en local.
- `rediapp` queda como referencia/soporte temporal.
- El backend está listo para continuar evolución sin romper el dump existente.

## Siguiente paso
Analizar y definir la **estrategia de modularidad hacia frontend en React**, respetando:
- Backend en Django
- Frontend desacoplado en React
- Transición progresiva desde el monolito anterior basado en templates HTML

Este análisis permitirá planificar la refactorización del frontend de forma ordenada y paulatina.
