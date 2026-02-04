📘 SRNI Platform
Fase Inicial – Frontend React
Documento técnico de integración Frontend (React) con Backend Django (Session + CSRF)
1️⃣ Objetivo de esta fase

Esta fase tuvo como objetivo:

Crear la base del frontend en React

Integrar correctamente la autenticación por sesión Django (NO JWT)

Replicar el comportamiento del frontend clásico (HTML + Django templates)

Definir un layout base reutilizable (equivalente a base.html)

Implementar un menú superior global

Establecer un flujo claro:

Login → Home → Dashboard / Módulos

Esta fase NO incluye aún:

React Router

CRUDs completos de módulos

Roles y permisos avanzados

2️⃣ Stack técnico
Frontend

React + Vite

Fetch API

Chart.js (para dashboard)

CSS plano (sin frameworks)

Backend

Django

Autenticación por sesión (sessionid)

Protección CSRF (csrftoken)

API REST interna (no pública)

3️⃣ Principios clave de la integración
❌ No se usa JWT
✅ Se usan cookies HTTP

Esto replica exactamente el comportamiento clásico de Django:

sessionid → identifica la sesión

csrftoken → protege operaciones sensibles

👉 Regla obligatoria
Toda llamada al backend debe usar:

credentials: "include"

4️⃣ Endpoints usados en el Frontend
Autenticación
Método	Endpoint	Uso
GET	/api/auth/csrf/	Inicializar cookie CSRF
POST	/api/auth/login/	Login
GET	/api/auth/me/	Verificar sesión
POST	/api/auth/logout/	Cerrar sesión
Dashboard
Método	Endpoint	Uso
GET	/api/dashboard/kpis/?limit=10	KPIs y gráficas
5️⃣ Flujo de autenticación en React
Paso 1 – Obtener CSRF

Se ejecuta antes de cualquier POST:

await fetch("/api/auth/csrf/", {
  credentials: "include",
});

Paso 2 – Login
fetch("/api/auth/login/", {
  method: "POST",
  credentials: "include",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": csrftoken,
  },
  body: JSON.stringify({ username, password }),
});

Paso 3 – Verificar sesión
fetch("/api/auth/me/", {
  credentials: "include",
});

Paso 4 – Logout
fetch("/api/auth/logout/", {
  method: "POST",
  credentials: "include",
  headers: {
    "X-CSRFToken": csrftoken,
  },
});

6️⃣ Estructura del frontend
frontend/
└── rni_front/
    ├── src/
    │   ├── api/
    │   │   ├── auth.js
    │   │   └── dashboard.js
    │   ├── layouts/
    │   │   └── AppLayout.jsx
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Home.jsx
    │   │   └── Dashboard.jsx
    │   ├── assets/
    │   │   ├── dashboard.css
    │   │   └── home.css
    │   └── App.jsx
    └── public/
        └── logo-unidad-victimas.png

7️⃣ Layout base (equivalente a base.html)
Archivo
src/layouts/AppLayout.jsx

Responsabilidad del Layout

Logo institucional

Título de la vista

Usuario autenticado

Botón cerrar sesión

Menú superior global

Contenedor central reutilizable

👉 Ninguna página repite header o estructura base

Uso típico
<AppLayout
  title="Inicio – Red Nacional de Información"
  username={username}
  onLogout={handleLogout}
  onGoHome={onGoHome}
  onGoDashboard={onGoDashboard}
  onGoSql={onGoSql}
  onGoColaboradores={onGoColaboradores}
  onGoAutomatizacion={onGoAutomatizacion}
>
  {/* contenido */}
</AppLayout>

8️⃣ Menú superior global

El menú se definió a nivel del layout, no por página.

Opciones disponibles

Inicio

Dashboard

Query SQL

Colaboradores

Automatización

Comportamiento

Funciona desde cualquier vista

Cambia la pantalla usando estado interno (screen)

No usa rutas aún

9️⃣ Navegación sin React Router (decisión intencional)

En esta fase se implementó un router simple por estado:

const [screen, setScreen] = useState("home");


Valores posibles:

home

dashboard

sql

colaboradores

automatizacion

Esto permite:

Flujo claro

Debug sencillo

Migración futura limpia a react-router-dom

🔟 Home (pantalla inicial tras login)
Función

Punto de entrada del sistema

Hub de navegación

Replica home.html clásico

Componentes

Header (layout)

Mensaje de bienvenida

Cards de acceso a módulos

1️⃣1️⃣ Dashboard
Funcionalidades

KPIs generales

Gráficas con Chart.js

Consumo del endpoint /api/dashboard/kpis/

Consideraciones técnicas

Se destruyen gráficas antes de recrearlas (chart.destroy())

maintainAspectRatio: false para control visual

Manejo de estado loading, error, data

1️⃣2️⃣ Seguridad

Cookies HTTPOnly (backend)

CSRF sincronizado

Sesión validada antes de renderizar vistas

Si me() falla → vuelve a Login

1️⃣3️⃣ Estado actual del frontend

✅ Login funcional
✅ Home funcional
✅ Dashboard funcional
✅ Menú global estable
✅ Arquitectura limpia y escalable

1️⃣4️⃣ Próximos pasos recomendados

Migrar navegación a react-router-dom

Implementar Query SQL real

Implementar Colaboradores (CRUD)

Control por roles

Manejo global de errores

Build de producción