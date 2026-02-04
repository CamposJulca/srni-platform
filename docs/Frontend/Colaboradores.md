 README – Fase Frontend React
Módulo: Colaboradores (Solo Lectura)
Proyecto

SRNI Platform – Frontend React

Estado

 Implementado
 Alcance actual: solo lectura (GET List)
 Sin creación, edición ni eliminación desde el frontend

1. Objetivo del módulo

Implementar en React la visualización del listado de colaboradores consumiendo el backend existente, respetando:

Autenticación por cookies de sesión

Contrato de datos del API

Estructura estándar de respuesta { ok, data, error }

Integración con layout y menú global de la aplicación

2. Arquitectura Frontend aplicada

El módulo de Colaboradores se integra a una arquitectura state-based navigation (sin react-router por ahora):

App.jsx
 ├── Login
 ├── Home
 ├── Dashboard
 └── Colaboradores


La navegación se controla por estado (screen) y callbacks (onGoColaboradores, etc.).

3. Endpoint consumido
GET – Listado de colaboradores
GET /api/colaboradores/?page=1&page_size=20

Respuesta real del backend
{
  "ok": true,
  "data": {
    "items": [
      {
        "id": 1,
        "cedula": "79996063",
        "nombres": "GELMAN ANDRES",
        "apellidos": "CARDENAS HERRERA",
        "estado": "ACTIVO",
        "fecha_creacion": "2026-01-16T09:19:16.484668-05:00"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 94,
      "total_pages": 5
    },
    "filters": {
      "q": "",
      "estado": ""
    }
  },
  "error": null
}


📌 Nota crítica:
El frontend NO recibe una lista directa.
La lista está dentro de:

response.data.items

4. Capa API (fetch)

Archivo:

src/api/colaboradores.js


Responsabilidades:

Construir query params (page, page_size, q, estado)

Incluir cookies de sesión (credentials: "include")

Validar estructura { ok: true }

Retornar solo data, no el wrapper completo

export async function getColaboradores({ page = 1, page_size = 20 } = {}) {
  const params = new URLSearchParams({ page, page_size });

  const res = await fetch(`/api/colaboradores/?${params.toString()}`, {
    credentials: "include",
  });

  const json = await res.json();

  if (!res.ok || !json?.ok) {
    throw new Error("No se pudieron cargar los colaboradores");
  }

  return json.data; // { items, pagination, filters }
}

5. Página Colaboradores (UI)

Archivo:

src/pages/Colaboradores.jsx

Responsabilidades

Obtener usuario autenticado (/api/auth/me)

Consumir listado de colaboradores

Renderizar tabla en modo solo lectura

Manejar estados:

loading

error

empty list

Integrarse al layout global y menú superior

Campos mostrados
Campo	Origen
Cédula	cedula
Nombres	nombres
Apellidos	apellidos
Estado	estado
Fecha creación	fecha_creacion

La fecha se formatea de forma segura y opcional.

6. Layout y navegación global

El módulo usa el AppLayout compartido:

src/layouts/AppLayout.jsx


Incluye:

Logo institucional

Título dinámico

Usuario autenticado

Menú superior global:

Inicio

Dashboard

Query SQL

Colaboradores

Automatización

Botón de logout

Esto garantiza consistencia visual y navegación uniforme en todo el frontend.

7. Manejo de autenticación

Todas las peticiones usan cookies de sesión

Si la sesión no es válida, el backend responde 401

El flujo general de autenticación ya está resuelto en App.jsx

Colaboradores asume sesión válida

8. Decisiones técnicas clave

 No se usa react-router aún (estado centralizado)

 No se replica lógica de backend

 No se usan mocks

✅ Se respeta contrato real del API

✅ Se separa capa API / UI


9. Estado actual

✔ Listado funcional
✔ Datos reales desde backend
✔ Integrado al menú global
✔ Estilo consistente con Dashboard y Home

 El módulo queda listo para evolución, sin deuda técnica.


Fin del documento
Frontend React – Colaboradores
SRNI Platform