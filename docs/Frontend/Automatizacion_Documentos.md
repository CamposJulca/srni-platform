README / Informe técnico – Frontend React

Módulo: Automatización Documental
 Esto es para copiar y pegar tal cual

Automatización Documental – Frontend (React)
Descripción general

Este módulo implementa en React el flujo completo de automatización documental para:

Carga masiva de documentos Word (.docx) en ZIP
Carga de firma digital en PNG
Posicionamiento visual de la firma sobre un PDF preview
Generación masiva de PDFs firmados
Descarga del ZIP final con todos los documentos firmados

El frontend está diseñado para trabajar con backend Django autenticado por sesión + CSRF, sin tokens externos.

Flujo funcional (UX real del usuario)
1. Cargar documentos y firma

El usuario sube:

Un archivo .zip que contiene uno o más .docx
Una imagen de firma en formato .png
Se envía al backend vía multipart/form-data

El sistema valida:

Que exista al menos un DOCX
Que la firma sea PNG
El estado se refleja en tiempo real en la UI y en el panel de logs

Endpoint usado:

POST /api/automatizacion/upload/

2. Preview PDF + posicionamiento de firma (Enfoque B – UX mejorado)

Después del upload, el frontend solicita al backend convertir un DOCX a PDF solo para preview
Ese PDF se muestra como fondo visual

Sobre ese PDF:

La firma (PNG) se puede arrastrar
Se puede redimensionar (esquina inferior derecha)
El frontend calcula ratios relativos:
x_ratio
y_ratio (desde abajo)
width_ratio
height_ratio
Estos ratios garantizan consistencia en todos los PDFs finales

Endpoints usados:

POST /api/automatizacion/preview/convert/
GET  /api/automatizacion/preview/pdf/
GET  /api/automatizacion/preview/firma/
POST /api/automatizacion/firma/position/

3. Generar y firmar PDFs

El frontend dispara el proceso completo:

Conversión de todos los DOCX → PDF
Aplicación de la firma en cada PDF usando los ratios guardados
El proceso es síncrono desde el punto de vista del usuario
El estado y errores se reflejan en el panel de logs

Endpoint:

POST /api/automatizacion/generate/

4. Descargar ZIP final

Una vez existen PDFs firmados:
Se habilita el botón de descarga
Se descarga un ZIP con todos los PDFs finales

Endpoint:

GET /api/automatizacion/download/

Arquitectura del Frontend
Componentes principales
Automatizacion.jsx
Controla el flujo completo (pasos 1 → 4)
Manejo de estados, validaciones y logs
PosicionarFirma.jsx
Canvas visual con PDF de fondo
Drag & resize de la firma
Cálculo de ratios relativos
API layer

Archivo:

src/api/automatizacion.js

Responsabilidades:

Manejo centralizado de llamadas fetch
Inclusión automática de cookies de sesión
Manejo de CSRF mediante getCSRF()
Parseo estándar { ok, data, error }
Seguridad
Autenticación por sesión Django
Protección CSRF en todos los POST
Uso de credentials: "include"

El PDF preview se sirve con:

X-Frame-Options: SAMEORIGIN

para permitir renderizado embebido