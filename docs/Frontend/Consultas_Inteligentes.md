Frontend React – QuerySQL & NLQuery (RNI)
Objetivo

Se implementaron en React dos módulos de consulta avanzada de datos:

QuerySQL → consultas SQL manuales, seguras y controladas.
NLQuery → consultas inteligentes (Lenguaje Natural → SQL), con fallback a SQL manual.

Ambos módulos consumen APIs backend existentes, funcionan con sesión autenticada, manejan CSRF, y están preparados para operar con o sin OpenAI API Key.
-------------------------------------------------------
Módulos implementados
1️⃣ QuerySQL (SQL manual seguro)

Ruta / Página

Página React: src/pages/QuerySQL.jsx
Acceso desde menú: Query SQL
-------------------------------------------------------
Propósito
Permitir a usuarios autorizados ejecutar consultas SELECT directamente sobre PostgreSQL, sin riesgo de modificación de datos.
-------------------------------------------------------
Reglas visibles para el usuario

Solo permite SELECT o WITH ... SELECT
No permite ; (múltiples sentencias)
Solo superusers pueden ejecutar
Errores se muestran en pantalla en formato claro
-------------------------------------------------------
Flujo funcional

Al cargar:

Se valida sesión (/api/auth/me/)
Se consulta estado DB (/api/analytics/health/)
Usuario escribe SQL manual
Click Consultar

Se ejecuta:

POST /api/analytics/sql/execute/
Se renderiza tabla dinámica con columnas y filas
Botón Limpiar reinicia estado
-------------------------------------------------------
Componentes clave

<textarea> SQL

Tabla dinámica <Table />
Pills de estado (DB OK / DB ERROR)
Manejo de busy, error, result
-------------------------------------------------------
2️⃣ NLQuery (NL → SQL → Run)

Ruta / Página
Página React: src/pages/NLQuery.jsx
Acceso desde menú: NLQuery
-------------------------------------------------------
Propósito
Permitir consultas:

Modo Manual (SQL seguro) → siempre disponible
Modo Inteligente (Lenguaje Natural) → disponible solo si OpenAI está configurado
-------------------------------------------------------
Estados del sistema
El frontend evalúa:

DB (db_ok)
Schema (schema_ok)
OpenAI (openai_configured)
Y los muestra como badges:

🟢 OK
🟠 WARNING
🔴 ERROR
-------------------------------------------------------
Flujos disponibles

Modo SQL Manual

El usuario escribe SQL directamente

Se ejecuta:

POST /api/nlquery/run/
Aplica mismas restricciones de seguridad que QuerySQL
-------------------------------------------------------
🔹 Modo NL → SQL (cuando OpenAI existe)

Usuario escribe pregunta en lenguaje natural
Click Generar SQL
POST /api/nlquery/generate-sql/
El SQL generado se muestra en textarea
Usuario puede editar o ejecutar
-------------------------------------------------------
🔹 Modo NL → SQL → Run

Ejecuta todo en un paso:

POST /api/nlquery/run/ { question }

-------------------------------------------------------
Fallback inteligente
Si OpenAI NO está configurado:

Botones NL se deshabilitan
Mensaje guía visible:
“OPENAI no está configurado. Puedes usar el modo SQL manual mientras.”
Botones de ayuda (UX agregado)
Se agregó un botón de ayuda contextual en:

QuerySQL
NLQuery
-------------------------------------------------------
Implementación

Componente reutilizable: src/components/HelpModal.jsx
Se abre como modal
No depende del backend
-------------------------------------------------------
Contenido del HelpModal
Explica en lenguaje simple:

Qué hace cada módulo
Qué puede y no puede hacer el usuario
Ejemplos de consultas válidas

Diferencia entre:
SQL manual
Consulta inteligente (NLQuery)
Mensajes claros sobre permisos y límites
-------------------------------------------------------
Objetivo UX
Que usuarios no técnicos entiendan:

Qué escribir
Qué esperar
Por qué algo puede fallar
Integración en AppLayout / Menú
-------------------------------------------------------
Archivo:

src/layouts/AppLayout.jsx
Se integraron los botones:

Inicio
Dashboard
Query SQL
NLQuery
Colaboradores
Automatización

Cada botón delega navegación vía props (onGoX), manteniendo el layout desacoplado.

Reglas técnicas importantes (Frontend)
Autenticación

Todas las llamadas usan:

fetch(url, { credentials: "include" })

CSRF

Antes de cualquier POST:

GET /api/auth/csrf/


Luego enviar:

X-CSRFToken: <token>
Manejo de errores
Errores backend → mostrados al usuario
No hay redirects silenciosos
No hay pantallas en blanco
-------------------------------------------------------
Dependencias / Requisitos
Para que NLQuery Inteligente funcione

⚠️ No es frontend, pero el frontend detecta el estado.

El líder debe configurar en backend:

OPENAI_API_KEY=xxxx


Sin esto:

NLQuery funciona solo en modo SQL manual

UI se mantiene estable y clara
-------------------------------------------------------
Estado final

✅ QuerySQL funcional
✅ NLQuery funcional (manual + inteligente cuando aplique)
✅ Seguridad respetada
✅ UX guiado con botones de ayuda
✅ Frontend desacoplado del backend
✅ Listo para producción