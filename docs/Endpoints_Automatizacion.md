# Automatización Documental – Backend API (listo para React)

## Objetivo
Se transformó el módulo de Automatización Documental, originalmente construido para consumo HTML, a una **API JSON compatible con React** usando:

- ✅ Django Session Auth (cookies `sessionid`)
- ✅ CSRF (cookie `csrftoken` + header `X-CSRFToken`)
- ❌ No JWT
- ✅ Respuesta estándar `{ok, data, error}`
- ✅ Trabajo por sesión: cada usuario tiene un `session_id` y directorios aislados en `MEDIA_ROOT`

---

## Flujo funcional (API)
1) **Health**: valida sesión y estado
2) **Upload**: recibe ZIP + firma (PNG), extrae docx
3) **Guardar posición**: guarda config de firma (ratios)
4) **Generate**: convierte DOCX→PDF y firma PDFs *(requiere LibreOffice en runtime)*
5) **Download**: entrega ZIP final de PDFs firmados

---

## Seguridad aplicada
- Endpoints requieren sesión autenticada: sin sesión → **401 JSON**
- No se usa `@csrf_exempt` en API: POST requiere CSRF real
- Los archivos se guardan por `session_id` en:
  `MEDIA_ROOT/automatizacion/sesiones/<session_id>/`

---

## Endpoints

### Health
`GET /api/automatizacion/health/`

Devuelve estado de sesión y archivos:
- `has_zip`
- `has_signature_image`
- `has_signature_config`
- conteos docx/pdf/firmados

---

### Upload ZIP + firma
`POST /api/automatizacion/upload/` (multipart)

Form fields:
- `zip_file` (zip con `.docx`)
- `firma_file` (png)

Respuesta:
- `201 Created`
- `total_docx`

---

### Guardar posición de firma
`POST /api/automatizacion/firma/position/` (JSON)

Payload ejemplo:
```json
{"page":1,"x_ratio":0.70,"y_ratio":0.10,"width_ratio":0.20,"height_ratio":0.10}

Preview info

GET /api/automatizacion/preview/

Devuelve:

pdfs_generated (vacío si no hay conversion)

has_signature_image

has_signature_config

endpoints de preview

Preview firma

GET /api/automatizacion/preview/firma/
Devuelve image/png (firma cargada)

Generate (convertir y firmar) – PENDIENTE de LibreOffice

POST /api/automatizacion/generate/

⚠️ Requiere binario libreoffice disponible en runtime para convertir .docx → .pdf.

Download ZIP final

GET /api/automatizacion/download/

Si no hay firmados:

400 NO_SIGNED_PDFS

Pruebas CURL (sin LibreOffice) – orden correcto
1) Health (200)
curl.exe -i -b .\cookies.txt "http://localhost:8000/api/automatizacion/health/"

2) Upload (201)
curl.exe -i -X POST "http://localhost:8000/api/automatizacion/upload/" `
  -b .\cookies.txt -c .\cookies.txt `
  -H "X-CSRFToken: $csrf" `
  -H "Origin: http://localhost:8000" `
  -H "Referer: http://localhost:8000/" `
  -F "zip_file=@tmp_upload/input.zip" `
  -F "firma_file=@tmp_upload/firma.png"

3) Guardar posición firma (200)
@'
{"page":1,"x_ratio":0.70,"y_ratio":0.10,"width_ratio":0.20,"height_ratio":0.10}
'@ | Set-Content -Encoding utf8 .\pos.json

curl.exe -i -X POST "http://localhost:8000/api/automatizacion/firma/position/" `
  -b .\cookies.txt -c .\cookies.txt `
  -H "Content-Type: application/json" `
  -H "X-CSRFToken: $csrf" `
  -H "Origin: http://localhost:8000" `
  -H "Referer: http://localhost:8000/" `
  --data-binary "@pos.json"

4) Preview info (200)
curl.exe -i -b .\cookies.txt "http://localhost:8000/api/automatizacion/preview/"

5) Preview firma (200 si hay firma cargada)
curl.exe -L -b .\cookies.txt -o .\firma_preview.png "http://localhost:8000/api/automatizacion/preview/firma/"

6) Download (400 esperado si aún no hay firmados)
curl.exe -i -b .\cookies.txt "http://localhost:8000/api/automatizacion/download/"


Resultado esperado:

400 NO_SIGNED_PDFS

Integración React

Siempre usar credentials: "include"

Antes de POST: GET /api/auth/csrf/

Enviar header: X-CSRFToken

Upload desde React:

usar FormData

fields: zip_file, firma_file

Pendiente para rama develop (habilitar Generate)

Instalar LibreOffice en runtime (Docker recomendado):

RUN apt-get update && \
    apt-get install -y libreoffice fontconfig fonts-dejavu && \
    rm -rf /var/lib/apt/lists/*

Luego:

docker compose -f backend/rni_web/docker-compose.yml up -d --build