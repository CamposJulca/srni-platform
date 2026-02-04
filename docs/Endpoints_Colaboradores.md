  # SRNI Platform - Backend Colaboradores (Guía de Pruebas + Endpoints para Frontend)

  ## Objetivo
  Este documento deja:
  1) La **secuencia de pruebas** con `curl` (PowerShell Windows) para validar auth + CSRF + CRUD de Colaboradores.
  2) La **documentación técnica** del módulo `apps/colaboradores/api.py`.
  3) Los **endpoints** y el contrato de datos para que el frontend en **React** consuma sin fricción.

  ---

  ## Requisitos
  - Backend corriendo en: `http://localhost:8000`
  - Autenticación por **session cookie** (`sessionid`) + **CSRF** (`csrftoken`)
  - `cookies.txt` se usa como jar de cookies para curl.

  > Regla de oro:
  > - Siempre: **CSRF -> Login -> refrescar CSRF -> requests mutantes (POST/PUT/PATCH/DELETE)**

  ---

  ## Secuencia de pruebas (PowerShell - ejecutar en este orden)

  ### 0) Limpieza
  ```powershell
  Remove-Item .\cookies.txt -ErrorAction SilentlyContinue
  Remove-Item .\login.json -ErrorAction SilentlyContinue
  Remove-Item .\patch.json -ErrorAction SilentlyContinue
  Remove-Item .\create.json -ErrorAction SilentlyContinue
  1) Crear archivos JSON (login / patch / create)
  powershell
  Copiar código
  @'
  {"username":"jorge","password":"jorge2025."}
  '@ | Set-Content -Encoding utf8 .\login.json
  powershell
  Copiar código
  @'
  {"estado":"ACTIVO"}
  '@ | Set-Content -Encoding utf8 .\patch.json
  powershell
  Copiar código
  @'
  {"cedula":"123456789","nombres":"PRUEBA","apellidos":"API","estado":"ACTIVO"}
  '@ | Set-Content -Encoding utf8 .\create.json
  2) Obtener CSRF inicial (crea csrftoken en cookies.txt)
  powershell
  Copiar código
  curl.exe -s -c .\cookies.txt "http://localhost:8000/api/auth/csrf/" | Out-Null
  $csrf = ((Select-String -Path .\cookies.txt -Pattern "csrftoken" | Select-Object -Last 1).Line -split "\s+")[-1]
  $csrf
  3) Login (setea sessionid y rota csrftoken)
  powershell
  Copiar código
  curl.exe -i -c .\cookies.txt -b .\cookies.txt `
    -H "Content-Type: application/json" `
    -H "X-CSRFToken: $csrf" `
    --data-binary "@login.json" `
    "http://localhost:8000/api/auth/login/"
  4) Refrescar CSRF DESPUÉS del login (obligatorio)
  powershell
  Copiar código
  $csrf = ((Select-String -Path .\cookies.txt -Pattern "csrftoken" | Select-Object -Last 1).Line -split "\s+")[-1]
  $csrf
  5) Verificar sesión (me)
  powershell
  Copiar código
  curl.exe -i -b .\cookies.txt "http://localhost:8000/api/auth/me/"
  Esperado: 200 OK y "authenticated": true.

  Pruebas módulo Colaboradores
  6) GET detail
  powershell
  Copiar código
  curl.exe -i -b .\cookies.txt "http://localhost:8000/api/colaboradores/1/"
  Esperado: 200 OK

  7) PATCH detail (update parcial)
  powershell
  Copiar código
  curl.exe -i -X PATCH "http://localhost:8000/api/colaboradores/1/" `
    -b .\cookies.txt -c .\cookies.txt `
    -H "Content-Type: application/json" `
    -H "X-CSRFToken: $csrf" `
    -H "Origin: http://localhost:8000" `
    -H "Referer: http://localhost:8000/" `
    --data-binary "@patch.json"
  Esperado: 200 OK

  8) GET list con paginación
  powershell
  Copiar código
  curl.exe -i -b .\cookies.txt "http://localhost:8000/api/colaboradores/?page=1&page_size=5"
  Esperado: 200 OK con items[] y pagination.

  9) GET list con filtro q
  powershell
  Copiar código
  curl.exe -i -b .\cookies.txt "http://localhost:8000/api/colaboradores/?q=GELMAN"
  10) GET list con filtro estado
  powershell
  Copiar código
  curl.exe -i -b .\cookies.txt "http://localhost:8000/api/colaboradores/?estado=ACTIVO"
  11) POST create
  powershell
  Copiar código
  curl.exe -i -X POST "http://localhost:8000/api/colaboradores/" `
    -b .\cookies.txt -c .\cookies.txt `
    -H "Content-Type: application/json" `
    -H "X-CSRFToken: $csrf" `
    -H "Origin: http://localhost:8000" `
    -H "Referer: http://localhost:8000/" `
    --data-binary "@create.json"
  Esperado: 201 Created

  Logout y validación final
  12) Logout
  powershell
  Copiar código
  curl.exe -i -X POST "http://localhost:8000/api/auth/logout/" `
    -b .\cookies.txt -c .\cookies.txt `
    -H "X-CSRFToken: $csrf" `
    -H "Origin: http://localhost:8000" `
    -H "Referer: http://localhost:8000/"
  Esperado: 200 OK

  13) Confirmar que ya no está autenticado
  powershell
  Copiar código
  curl.exe -i -b .\cookies.txt "http://localhost:8000/api/auth/me/"
  Esperado: 401 Unauthorized con { code: "NOT_AUTHENTICATED" }

  Documentación técnica - Backend Colaboradores
  Archivo
  apps/colaboradores/api.py

  Modelo usado
  core.models.ColaboradorCore (tabla: colaborador_core)

  Serialización
  Respuesta de colaborador:

  json
  Copiar código
  {
    "id": 1,
    "cedula": "79996063",
    "nombres": "GELMAN ANDRES",
    "apellidos": "CARDENAS HERRERA",
    "estado": "ACTIVO",
    "fecha_creacion": "2026-01-16T09:19:16.484668-05:00"
  }
  Nota:

  fecha_creacion puede venir null en algunos registros (front debe manejarlo como opcional).

  Envoltura estándar de respuestas
  OK:

  json
  Copiar código
  { "ok": true, "data": <payload>, "error": null }
  Error:

  json
  Copiar código
  { "ok": false, "data": null, "error": { "code": "SOME_CODE", "message": "..." } }
  Endpoints (para React)
  Auth
  1) Obtener CSRF
  GET /api/auth/csrf/

  Devuelve token en body y setea cookie csrftoken.

  El front debe guardar el token (o leer cookie) para enviarlo en X-CSRFToken.

  2) Login
  POST /api/auth/login/
  Body:

  json
  Copiar código
  { "username": "jorge", "password": "jorge2025." }
  Respuesta: ok=true y setea cookie sessionid.

  3) Estado de sesión
  GET /api/auth/me/

  200 si autenticado

  401 si no autenticado

  4) Logout
  POST /api/auth/logout/

  Colaboradores
  1) List + filtros (GET)
  GET /api/colaboradores/?page=1&page_size=20&q=texto&estado=ACTIVO

  page default: 1

  page_size default: 20

  q: filtra por nombres, apellidos, cedula

  estado: match exact (case-insensitive)

  Respuesta:

  json
  Copiar código
  {
    "ok": true,
    "data": {
      "items": [ { ...colaborador }, ... ],
      "pagination": { "page": 1, "page_size": 20, "total": 93, "total_pages": 5 },
      "filters": { "q": "", "estado": "" }
    },
    "error": null
  }
  2) Detail (GET)
  GET /api/colaboradores/<id>/

  Respuesta: colaborador.

  3) Create (POST)
  POST /api/colaboradores/
  Body:

  json
  Copiar código
  { "cedula":"123", "nombres":"A", "apellidos":"B", "estado":"ACTIVO" }
  Errores esperados:

  400 VALIDATION_ERROR si faltan campos.

  409 DUPLICATE si cedula ya existe.

  4) Update completo (PUT)
  PUT /api/colaboradores/<id>/
  Body (enviar todos):

  json
  Copiar código
  { "cedula":"...", "nombres":"...", "apellidos":"...", "estado":"ACTIVO" }
  5) Update parcial (PATCH)
  PATCH /api/colaboradores/<id>/
  Body (solo lo que cambie):

  json
  Copiar código
  { "estado":"INACTIVO" }
  6) Delete
  DELETE /api/colaboradores/<id>/
  Respuesta:

  json
  Copiar código
  { "ok": true, "data": { "deleted": true, "id": 10 }, "error": null }
  Guía corta para React (fetch/axios)
  Reglas para que funcione con cookies + CSRF
  En requests usar credentials: "include" (fetch) o withCredentials: true (axios).

  Obtener CSRF primero con /api/auth/csrf/.

  Enviar header X-CSRFToken con el token.

  Login rota CSRF: después del login, volver a pedir CSRF o leer el csrftoken actualizado.

  Ejemplo con fetch (esqueleto)
  GET CSRF:

  fetch("/api/auth/csrf/", { credentials:"include" })

  LOGIN:

  fetch("/api/auth/login/", { method:"POST", credentials:"include", headers:{ "Content-Type":"application/json","X-CSRFToken":token }, body: JSON.stringify({username,password}) })

  PATCH:

  fetch("/api/colaboradores/1/", { method:"PATCH", credentials:"include", headers:{ "Content-Type":"application/json","X-CSRFToken":token }, body: JSON.stringify({estado:"ACTIVO"}) })

  Checklist de integración (Front)
  Puede hacer GET /api/auth/csrf/ y recibe cookie csrftoken

  Puede hacer POST /api/auth/login/ y recibe sessionid

  Puede hacer GET /api/auth/me/ y ve authenticated true

  Puede consumir /api/colaboradores/ list + filtros

  Puede hacer PATCH/POST con X-CSRFToken + cookies

  Logout invalida sesión y /api/auth/me/ retorna 401

  Estado
  Backend de Colaboradores: OK, autenticación por sesión y protección CSRF operando.
  Listo para integrar React sin dependencias adicionales.