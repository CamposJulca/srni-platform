# SRNI Platform — Dashboard API (KPIs) 

Documento para validar y consumir el **Dashboard KPIs** desde frontend (React) usando **sesión de Django** + **CSRF**.

- ❌ No JWT
- ✅ Cookies (`sessionid`, `csrftoken`)
- ✅ Compatible con React usando `credentials: "include"`

---

## 1) Conceptos clave (no negociables)

- Todo `POST` requiere **CSRF válido**.
- El CSRF puede **rotar después del login**.
- El header `X-CSRFToken` **debe coincidir** con la cookie `csrftoken`.
- Para React: **SIEMPRE** `credentials: "include"`.

El endpoint de dashboard es **GET**, pero requiere sesión (login), por lo tanto debe viajar cookie `sessionid`.

---

## 2) Endpoints involucrados

| Método | Endpoint | Descripción |
|------|---------|------------|
| GET | `/api/auth/csrf/` | Forzar cookie `csrftoken` |
| POST | `/api/auth/login/` | Login (crea sesión y cookie `sessionid`) |
| GET | `/api/auth/me/` | Verificar sesión activa |
| POST | `/api/auth/logout/` | Cerrar sesión |
| GET | `/api/dashboard/kpis/` | KPIs del dashboard (requiere sesión) |

---

## 3) Pruebas locales (PowerShell + curl.exe)

> Estas pruebas validan backend **sin frontend**.

### 3.1 Limpiar cookies previas
```powershell
Remove-Item .\cookies.txt -ErrorAction SilentlyContinue
Remove-Item .\login.json -ErrorAction SilentlyContinue
3.2 Obtener CSRF (obligatorio antes de login)
powershell
Copiar código
curl.exe -i -c cookies.txt "http://localhost:8000/api/auth/csrf/"
Resultado esperado

HTTP/1.1 200 OK

Header: Set-Cookie: csrftoken=...

Body:

json
Copiar código
{"ok": true, "data": {"status": "ok"}, "error": null}
3.3 Extraer CSRF desde cookies.txt (tomar el ÚLTIMO)
powershell
Copiar código
$csrf = (Get-Content .\cookies.txt |
  Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } |
  Select-Object -Last 1).Split("`t")[-1]

$csrf
3.4 Login (crea sesión sessionid)
powershell
Copiar código
Set-Content -NoNewline -Encoding ascii .\login.json '{"username":"jorge","password":"jorge2025."}'

curl.exe -i -b cookies.txt -c cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  --data-binary "@login.json" `
  "http://localhost:8000/api/auth/login/"
Resultado esperado

HTTP/1.1 200 OK

Headers Set-Cookie:

sessionid=...

csrftoken=... (puede rotar)

Body:

json
Copiar código
{"ok": true, "data": {"authenticated": true, "id": 1, "username": "jorge", "email": ""}, "error": null}
3.5 Verificar sesión activa
powershell
Copiar código
curl.exe -i -b cookies.txt "http://localhost:8000/api/auth/me/"
Resultado esperado

json
Copiar código
{"ok": true, "data": {"authenticated": true, "id": 1, "username": "jorge", "email": ""}, "error": null}
3.6 Probar Dashboard KPIs (con sesión)
powershell
Copiar código
curl.exe -i -b cookies.txt "http://localhost:8000/api/dashboard/kpis/"
Resultado esperado

HTTP/1.1 200 OK

JSON con estructura estándar:

Ejemplo real validado:

json
Copiar código
{
  "ok": true,
  "data": {
    "total_colaboradores": 92,
    "colaboradores_activos": 92,
    "total_contratos": 0,
    "valor_total_contratado": 0,
    "equipos": { "labels": [], "data": [] },
    "actividades_top": {
      "labels": ["ANGIE CAROLINA", "GUSTAVO ALONSO", "..."],
      "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
  },
  "error": null
}
3.7 Probar Dashboard KPIs (sin sesión)
powershell
Copiar código
curl.exe -i "http://localhost:8000/api/dashboard/kpis/"
Resultado esperado

HTTP/1.1 401 Unauthorized

Body:

json
Copiar código
{"ok": false, "data": null, "error": {"code": "NOT_AUTHENTICATED", "message": "Not authenticated."}}
3.8 Probar límite de Top (para frontend)
El endpoint soporta ?limit=<n>.

powershell
Copiar código
curl.exe -i -b cookies.txt "http://localhost:8000/api/dashboard/kpis/?limit=5"
Resultado esperado

actividades_top.labels y actividades_top.data con 5 elementos.

3.9 Logout (cierre de sesión)
Requiere CSRF en header.

powershell
Copiar código
$csrf = (Get-Content .\cookies.txt |
  Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } |
  Select-Object -Last 1).Split("`t")[-1]

curl.exe -i -b cookies.txt -c cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  --data-binary "{}" `
  "http://localhost:8000/api/auth/logout/"
Resultado esperado

HTTP/1.1 200 OK

Cookie sessionid expirada

Body:

json
Copiar código
{"ok": true, "data": {"status": "logged_out"}, "error": null}
4) Payload del Dashboard KPIs (contrato)
GET /api/dashboard/kpis/
Respuesta 200

json
Copiar código
{
  "ok": true,
  "data": {
    "total_colaboradores": 0,
    "colaboradores_activos": 0,
    "total_contratos": 0,
    "valor_total_contratado": 0,
    "equipos": { "labels": [], "data": [] },
    "actividades_top": { "labels": [], "data": [] }
  },
  "error": null
}
Significado de campos
total_colaboradores: conteo de colaboradores.

colaboradores_activos: conteo de colaboradores con estado activo (comparación case-insensitive).

total_contratos: conteo de contratos (según dataset local).

valor_total_contratado: actualmente 0 (dataset contrato_core no contiene columna monetaria).

equipos: distribución por equipos. Puede venir vacío si no existe tabla/relación.

actividades_top: top-N por actividades. Puede dar 0 si tabla actividad está vacía.

5) Reglas para frontend (React)
5.1 Cookies obligatorias
Para que viaje sessionid y csrftoken:

js
Copiar código
fetch("http://localhost:8000/api/dashboard/kpis/", {
  method: "GET",
  credentials: "include",
});
5.2 Flujo recomendado
Al cargar login:

GET /api/auth/csrf/ (setea csrftoken)

Login:

POST /api/auth/login/ con X-CSRFToken y credentials: "include"

Proteger rutas:

GET /api/auth/me/

Dashboard:

GET /api/dashboard/kpis/?limit=10

Logout:

POST /api/auth/logout/ con X-CSRFToken

6) Errores comunes y causa
Error	Causa
401 NOT_AUTHENTICATED en dashboard	No hay cookie sessionid (no se hizo login o no se envían cookies)
403 CSRF en login/logout	X-CSRFToken no coincide con cookie csrftoken, o CSRF rotó y no se actualizó
Dashboard devuelve ceros en contratos	Dataset local sin contratos en contrato_core
Dashboard equipos vacío	No existe tabla/relación de equipos en la DB local

7) Ubicación del código (backend)
API dashboard: backend/rni_web/src/apps/dashboard/api.py

Services dashboard: backend/rni_web/src/apps/dashboard/services.py

Rutas API dashboard: backend/rni_web/src/apps/dashboard/urls_api.py

Router principal: backend/rni_web/src/config/urls.py

8) Estado validado
Login por sesión Django funcionando.
Endpoint /api/dashboard/kpis/ funcionando y protegido.
Soporte ?limit=<n> validado.
Payload consistente para React.