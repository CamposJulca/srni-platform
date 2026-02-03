# NLQuery Backend (NL2SQL) – Documentación técnica para integración con React

## Objetivo
Se dejó implementado el módulo **NLQuery** en el backend Django para soportar un flujo **NL → SQL → ejecución en DB**, con seguridad básica (solo SELECT) y contrato JSON estándar para consumo futuro desde **React**.

Actualmente funciona **sin API Key** gracias al endpoint `health`, y queda listo para que cuando se disponga de `OPENAI_API_KEY`, la integración con OpenAI se active sin cambios adicionales de código (solo configuración por variables de entorno).

---

## Qué se implementó

### 1) Endpoints nuevos del módulo `nlquery`
Se agregaron endpoints bajo el prefijo `/api/nlquery/`:

- `GET  /api/nlquery/health/`
- `GET  /api/nlquery/schema/`
- `POST /api/nlquery/run/`
- `POST /api/nlquery/generate-sql/` (requiere OpenAI API Key)
- `POST /api/nlquery/run/` (modo NL → SQL → run requiere API Key si se envía `question`)

### 2) Contrato de respuesta estándar (igual que colaboradores/dashboard)
Todas las respuestas siguen el formato:
```json
{
  "ok": true|false,
  "data": {...} | null,
  "error": { "code": "...", "message": "..." } | null
}
3) Seguridad básica
El endpoint /run/ valida que la consulta sea solo SELECT (o WITH ... SELECT):

Bloquea keywords peligrosas (DROP, DELETE, UPDATE, etc.)

Bloquea múltiples statements (si aparece ;)

4) Endpoint health (clave sin OpenAI)
Se agregó GET /api/nlquery/health/ para validar que:

DB está OK (db_ok)

el schema whitelist carga (schema_ok)

cuántas tablas whitelist hay (schema_tables)

si OpenAI está configurado (openai_configured)

Esto permite pruebas completas del backend sin depender de API Key.

Configuración de OpenAI (cuando se tenga API Key)
Opción A (Docker Compose) – recomendado en ambientes Docker
En backend/rni_web/docker-compose.yml (servicio backend), agregar:

yml
Copiar código
environment:
  - OPENAI_API_KEY=TU_API_KEY_AQUI
Luego reconstruir:

bash
Copiar código
docker compose -f backend/rni_web/docker-compose.yml down
docker compose -f backend/rni_web/docker-compose.yml up -d --build
Opción B (.env)
Crear/editar .env:

env
Copiar código
OPENAI_API_KEY=TU_API_KEY_AQUI
Referenciarlo en docker-compose.yml:

yml
Copiar código
env_file:
  - .env
Rebuild igual que arriba.

Opción C (local/venv, sin Docker)
En PowerShell (solo para esa sesión):

powershell
Copiar código
$env:OPENAI_API_KEY="TU_API_KEY_AQUI"
python manage.py runserver
Pruebas con curl (paso a paso, numeradas)
Requisitos:

Backend corriendo en http://localhost:8000

Usuario existente para login (ejemplo: jorge / jorge2025.)

Ejecutar en PowerShell usando curl.exe

1) Limpiar archivos previos
powershell
Copiar código
Remove-Item .\cookies.txt -ErrorAction SilentlyContinue
Remove-Item .\login.json -ErrorAction SilentlyContinue
Remove-Item .\run.json -ErrorAction SilentlyContinue
2) Crear JSON de login
powershell
Copiar código
@'
{"username":"jorge","password":"jorge2025."}
'@ | Set-Content -Encoding utf8 .\login.json
3) Obtener CSRF inicial (guarda cookie csrftoken)
powershell
Copiar código
curl.exe -s -c .\cookies.txt "http://localhost:8000/api/auth/csrf/" | Out-Null
4) Extraer el token CSRF desde cookies.txt
powershell
Copiar código
$csrf = (Get-Content .\cookies.txt |
  Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } |
  Select-Object -Last 1).Split("`t")[-1]
$csrf
5) Login (crea sessionid)
powershell
Copiar código
curl.exe -i -c .\cookies.txt -b .\cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  --data-binary "@login.json" `
  "http://localhost:8000/api/auth/login/"
6) Refrescar CSRF después del login (recomendado)
powershell
Copiar código
curl.exe -s -b .\cookies.txt -c .\cookies.txt "http://localhost:8000/api/auth/csrf/" | Out-Null

$csrf = (Get-Content .\cookies.txt |
  Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } |
  Select-Object -Last 1).Split("`t")[-1]
$csrf
7) Verificar sesión (me)
powershell
Copiar código
curl.exe -i -b .\cookies.txt "http://localhost:8000/api/auth/me/"
Esperado: 200 OK y authenticated: true.

Pruebas NLQuery (SIN OpenAI)
8) Health check (valida DB + schema + si hay API key)
powershell
Copiar código
curl.exe -i -b .\cookies.txt "http://localhost:8000/api/nlquery/health/"
Esperado: 200 OK y:

db_ok: true

schema_ok: true

openai_configured: false (hasta que se configure API key)

9) Obtener schema (whitelist de tablas/columnas disponibles)
powershell
Copiar código
curl.exe -i -b .\cookies.txt "http://localhost:8000/api/nlquery/schema/"
Esperado: 200 OK y un JSON con schema.

10) Ejecutar SQL manual seguro (sin OpenAI)
Crear run.json:

powershell
Copiar código
@'
{"sql":"SELECT 1 as ok"}
'@ | Set-Content -Encoding utf8 .\run.json
Ejecutar:

powershell
Copiar código
curl.exe -i -X POST "http://localhost:8000/api/nlquery/run/" `
  -b .\cookies.txt -c .\cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  -H "Origin: http://localhost:8000" `
  -H "Referer: http://localhost:8000/" `
  --data-binary "@run.json"
Esperado: 200 OK y rows: [[1]].

Pruebas NLQuery (CON OpenAI, cuando exista API Key)
11) Generar SQL desde lenguaje natural
Crear q.json:

powershell
Copiar código
@'
{"question":"lista 5 registros de la tabla actividad"}
'@ | Set-Content -Encoding utf8 .\q.json
Ejecutar:

powershell
Copiar código
curl.exe -i -X POST "http://localhost:8000/api/nlquery/generate-sql/" `
  -b .\cookies.txt -c .\cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  -H "Origin: http://localhost:8000" `
  -H "Referer: http://localhost:8000/" `
  --data-binary "@q.json"
12) NL → SQL → Run (en un solo endpoint)
powershell
Copiar código
curl.exe -i -X POST "http://localhost:8000/api/nlquery/run/" `
  -b .\cookies.txt -c .\cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  -H "Origin: http://localhost:8000" `
  -H "Referer: http://localhost:8000/" `
  --data-binary "@q.json"
Si no hay API key configurada, debe responder error controlado con OPENAI_NOT_CONFIGURED (503).

Notas para el equipo de Frontend (React)
Usar fetch(..., { credentials: "include" }) para que el navegador mande cookies (sessionid, csrftoken).

Antes de POST, obtener CSRF con:

GET /api/auth/csrf/

En cada POST enviar header:

X-CSRFToken: <csrftoken>

Endpoints importantes para React:

GET /api/auth/me/ → sesión actual

GET /api/nlquery/health/ → readiness (ideal para pantalla de estado)

GET /api/nlquery/schema/ → debug / soporte

POST /api/nlquery/run/ → ejecución

POST /api/nlquery/generate-sql/ → obtener SQL (cuando haya API key)

Estado actual
✅ Backend NLQuery operativo y probado:

health 200 OK

schema 200 OK

run 200 OK con SELECT 1
⏳ OpenAI pendiente únicamente de configurar OPENAI_API_KEY.