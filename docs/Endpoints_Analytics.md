.

# Analytics Backend – Documentación Técnica (API segura para React)

## Objetivo
Se implementó el módulo **Analytics** como una **API backend segura**, preparada para ser consumida por un frontend en **React**, permitiendo la ejecución de consultas **SELECT** controladas sobre la base de datos, con protección contra comandos destructivos y con autenticación por sesión.

Este módulo **NO permite modificaciones de datos** y está blindado contra SQL peligroso, incluso para usuarios superuser.

---

## Qué se implementó

### 1) API Analytics (API-first, sin HTML)
Se dejó Analytics como **API pura**, sin redirects ni dependencias de templates HTML.

Endpoints expuestos bajo:


/api/analytics/


Todos los endpoints:
- Requieren **sesión autenticada**
- Devuelven JSON estándar `{ok, data, error}`
- Son compatibles con `fetch` desde React (`credentials: "include"`)

---

### 2) Seguridad implementada (CRÍTICO)

Se implementaron **tres capas de seguridad**, en este orden:

#### Capa 1 – Autenticación (API-first)
- Si no hay sesión → **401 JSON**
- No hay redirects a `/accounts/login/`
- Ideal para frontend SPA (React)

#### Capa 2 – Validación estricta de SQL
Solo se permite:
- `SELECT ...`
- `WITH ... SELECT ...` (CTE)

Se bloquea automáticamente:
- `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, etc.
- Múltiples statements (`;`)
- Cualquier SQL que no empiece por `SELECT` o `WITH`

 **Incluso siendo superuser, un `DROP TABLE` nunca se ejecuta.**

#### Capa 3 – Permisos
- El endpoint de ejecución de SQL libre está restringido a **superusers**
- Usuarios normales reciben `403 FORBIDDEN` aunque el SQL sea válido

---

## Endpoints disponibles

### 1) Health Check
Verifica que el módulo esté operativo y la DB conectada.



GET /api/analytics/health/


Respuesta:
```json
{
  "ok": true,
  "data": {
    "db_ok": true
  },
  "error": null
}

2) Ejecutar SQL (solo SELECT, solo superuser)
POST /api/analytics/sql/execute/


Payload:

{
  "sql": "SELECT 1 as ok"
}


Respuesta exitosa (200 OK):

{
  "ok": true,
  "data": {
    "sql": "SELECT 1 as ok",
    "result": {
      "columns": ["ok"],
      "rows": [[1]]
    }
  },
  "error": null
}


Errores posibles:

401 NOT_AUTHENTICATED

403 FORBIDDEN (usuario no superuser)

400 SQL_NOT_ALLOWED (SQL no permitido)

Pruebas con curl (PASO A PASO)

Requisitos:

Backend corriendo en http://localhost:8000

Usuario autenticado (ej: jorge)

Usuario superuser

PowerShell + curl.exe

1️⃣ Obtener CSRF
curl.exe -s -c .\cookies.txt "http://localhost:8000/api/auth/csrf/" | Out-Null


Extraer token:

$csrf = (Get-Content .\cookies.txt |
  Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } |
  Select-Object -Last 1).Split("`t")[-1]

2️⃣ Login
Set-Content -NoNewline -Encoding ascii .\login.json '{"username":"jorge","password":"jorge2025."}'

curl.exe -i -b .\cookies.txt -c .\cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  --data-binary "@login.json" `
  "http://localhost:8000/api/auth/login/"


Refrescar CSRF:

curl.exe -s -b .\cookies.txt -c .\cookies.txt "http://localhost:8000/api/auth/csrf/" | Out-Null
$csrf = (Get-Content .\cookies.txt |
  Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } |
  Select-Object -Last 1).Split("`t")[-1]

3️⃣ Health Check (200 OK)
curl.exe -i -b .\cookies.txt "http://localhost:8000/api/analytics/health/"


Resultado esperado:

200 OK

"db_ok": true

4️⃣ Ejecutar SQL válido (200 OK)

Crear payload:

@'
{"sql":"SELECT 1 as ok"}
'@ | Set-Content -Encoding utf8 .\a.json


Ejecutar:

curl.exe -i -X POST "http://localhost:8000/api/analytics/sql/execute/" `
  -b .\cookies.txt -c .\cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  -H "Origin: http://localhost:8000" `
  -H "Referer: http://localhost:8000/" `
  --data-binary "@a.json"


Resultado:

200 OK

Devuelve columnas y filas

5️⃣ Prueba de seguridad (400 SQL_NOT_ALLOWED)
@'
{"sql":"DROP TABLE actividad"}
'@ | Set-Content -Encoding utf8 .\a.json


Ejecutar mismo curl anterior.

Resultado esperado:

{
  "ok": false,
  "error": {
    "code": "SQL_NOT_ALLOWED",
    "message": "Only SELECT statements are allowed."
  }
}


Status: 400

✔️ Confirmación de que el backend está blindado.

Indicaciones para el Frontend (React)
Autenticación

Usar fetch con:

credentials: "include"

CSRF

Obtener token:

GET /api/auth/csrf/


Enviar en headers:

"X-CSRFToken": csrftoken

Endpoints a consumir

GET /api/auth/me/

GET /api/analytics/health/

POST /api/analytics/sql/execute/

Estado final

 Analytics backend completamente funcional
 Seguridad validada (200 / 400 / 403 correctos)
 Listo para integración con React
 Sin riesgo de daño a la base de datos