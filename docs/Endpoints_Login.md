# SRNI Platform — Autenticación por API (Django Session + CSRF)

Este backend utiliza **autenticación por sesión de Django** (`sessionid`) y protege los endpoints `POST` con **CSRF** (`csrftoken`).

- ❌ No JWT  
- ✅ Cookies HTTP  
- ✅ Compatible con React usando `credentials: "include"`

---

## Conceptos clave (imprescindible)
- Todo `POST` requiere **CSRF válido**
- El CSRF **rota después del login**
- El header `X-CSRFToken` **debe coincidir** con la cookie `csrftoken`
- Cookies y CSRF **deben venir de la misma sesión**
- En frontend: **SIEMPRE** usar `credentials: "include"`

---

## Endpoints disponibles

| Método | Endpoint | Descripción |
|------|--------|------------|
| GET | `/api/auth/csrf/` | Forzar cookie `csrftoken` |
| POST | `/api/auth/login/` | Login y creación de sesión |
| GET | `/api/auth/me/` | Verificar sesión activa |
| POST | `/api/auth/logout/` | Cerrar sesión |

---

## Pruebas locales con PowerShell + curl.exe

Estas pruebas validan el backend **sin frontend**.

---
comandos:

limipieza
Remove-Item .\cookies.txt -ErrorAction SilentlyContinue
Remove-Item .\login.json -ErrorAction SilentlyContinue

validar conexion backend
curl.exe -i "http://localhost:8000/api/auth/csrf/"


curl.exe -i -c cookies.txt "http://localhost:8000/api/auth/csrf/"

token
$csrf = (Get-Content .\cookies.txt |
  Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } |
  Select-Object -Last 1).Split("`t")[-1]

$csrf

login
Set-Content -NoNewline -Encoding ascii .\login.json '{"username":"jorge","password":"jorge2025."}'

curl.exe -i -b cookies.txt -c cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  --data-binary "@login.json" `
  "http://localhost:8000/api/auth/login/"

validar conexion
curl.exe -i -b cookies.txt "http://localhost:8000/api/auth/me/"

logout
curl.exe -i -b cookies.txt -c cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  --data-binary "{}" `
  "http://localhost:8000/api/auth/logout/"
---


### 1) Limpiar cookies previas
```powershell
Remove-Item .\cookies.txt -ErrorAction SilentlyContinue
2) Obtener CSRF (obligatorio antes de cualquier POST)
powershell
Copiar código
curl.exe -i -c cookies.txt "http://localhost:8000/api/auth/csrf/"
Resultado esperado

HTTP/1.1 200 OK

Header Set-Cookie: csrftoken=...

Body:

json
Copiar código
{"ok": true, "data": {"status": "ok"}, "error": null}
3) Extraer CSRF correctamente desde cookies.txt
⚠️ Siempre tomar el último csrftoken, no el primero.

powershell
Copiar código
$csrf = (Get-Content .\cookies.txt | Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } | Select-Object -Last 1).Split("`t")[-1]
4) Login (crea sesión)
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

Cookies:

sessionid=...

csrftoken=... (nuevo)

Body:

json
Copiar código
{"ok": true, "data": {"authenticated": true, "id": 1, "username": "jorge", "email": ""}, "error": null}
5) (Recomendado) Solicitar CSRF nuevamente después del login
Django puede rotar el CSRF tras autenticación.

powershell
Copiar código
curl.exe -i -b cookies.txt -c cookies.txt "http://localhost:8000/api/auth/csrf/"

$csrf = (Get-Content .\cookies.txt | Where-Object { $_ -match "`tcsrftoken`t" -and $_ -notmatch "^#" } | Select-Object -Last 1).Split("`t")[-1]
6) Verificar sesión activa
powershell
Copiar código
curl.exe -i -b cookies.txt "http://localhost:8000/api/auth/me/"
Resultado esperado

json
Copiar código
{"ok": true, "data": {"authenticated": true, ...}, "error": null}
7) Logout (cierre de sesión)
powershell
Copiar código
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
Reglas obligatorias para el Frontend (React)
Siempre usar cookies
js
Copiar código
fetch(url, {
  method: "POST",
  credentials: "include",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": csrftoken,
  },
  body: JSON.stringify(data),
});
Flujo correcto en React
GET /api/auth/csrf/ al cargar la app o login

Leer cookie csrftoken

POST /api/auth/login/

Guardar estado autenticado

Proteger rutas con GET /api/auth/me/

Logout con POST /api/auth/logout/

Errores comunes y causa
Error	Causa
403 CSRF	Token incorrecto o desincronizado
401 login	Credenciales inválidas
401 me	No hay sesión activa
Login funciona, logout falla	CSRF no se volvió a solicitar

Ubicación del código
Lógica API: backend/rni_web/src/apps/accounts/api.py

Rutas: backend/rni_web/src/apps/accounts/urls_api.py

Router principal: backend/rni_web/src/config/urls.py

Conclusión
Este flujo es determinístico, seguro y estable.
Si se siguen estos pasos no hay errores intermitentes ni comportamientos inconsistentes entre backend y frontend.