SINAPSIS – Frontend React
-----------------------------------------
Dashboard Analítico de Proyectos Tecnológicos (RNI)

-----------------------------------------
Descripción general

Este módulo corresponde al frontend en React del sistema SINAPSIS, encargado de visualizar y analizar el portafolio de proyectos tecnológicos de la Red Nacional de Información.

El frontend consume una API institucional y presenta la información en gráficas analíticas y tablas explorables, sin lógica de negocio ni normalización en el cliente.

-----------------------------------------
Arquitectura (Frontend)
Backend SINAPSIS (API REST)
        ↓
Fetch HTTP (React)
        ↓
Componentes Analíticos
        ↓
Dashboard Visual (Recharts)

-----------------------------------------
Estructura de archivos relevantes
src/
├── pages/
│   ├── SinapsisDashboard.jsx   # Dashboard principal
│   └── SinapsisExplorer.jsx    # Explorador técnico (debug / inspección)
│
├── components/
│   └── SinapsisCharts.jsx      # Gráficas reutilizables
│
├── api/
│   └── sinapsisApi.js          # Capa de consumo API

-----------------------------------------
Componentes del Frontend
1️⃣ SinapsisDashboard.jsx

Responsabilidad:

Cargar proyectos desde la API
Agregar información por categorías
Renderizar visualizaciones analíticas

Visualizaciones incluidas:

Proyectos por estado
Proyectos por ciclo de vida
Proyectos por nivel de riesgo
Proyectos por nivel de iniciativa
Tabla detallada de proyectos

Librerías usadas:

recharts
useEffect / useState

2️⃣ SinapsisExplorer.jsx

Uso técnico / exploratorio
Carga un snapshot local (projects_snapshot_*.json)
Permite inspeccionar la estructura real de los datos

No depende del backend
⚠️ Este componente es auxiliar, útil para desarrollo y validación de esquemas.

3️⃣ SinapsisCharts.jsx

Componente reutilizable
Gráficas desacopladas
Función countBy para agregaciones simples
Usado como base para futuras extensiones

4️⃣ sinapsisApi.js
GET /api/sinapsis/projects/


Encapsula el acceso a la API
Maneja errores de carga
No contiene lógica de transformación

-----------------------------------------
🧪 Flujo de ejecución

El usuario ingresa al módulo SINAPSIS
React ejecuta fetchProjects()
La API responde con el listado de proyectos

El frontend:

Agrega datos por categoría
Renderiza gráficas y tablas
No hay persistencia ni cache en cliente

-----------------------------------------
Decisiones de diseño

❌ Sin lógica de negocio en frontend
✅ Normalización y agregación mínima (solo conteos)
✅ Visualización reactiva
✅ Preparado para filtros, KPIs y exportaciones futuras
✅ Desacoplamiento total del origen de datos

-----------------------------------------
Dependencias técnicas

React + Vite
Recharts
API REST institucional SINAPSIS
⚠️ Nota importante – MongoDB
-----------------------------------------
Estado actual en desarrollo:
El backend SINAPSIS depende de MongoDB
En entorno local NO está configurado MONGO_URI

-----------------------------------------
Por esta razón, el endpoint:
GET /api/sinapsis/projects/
retorna HTTP 500 en desarrollo

Esto es esperado y no corresponde a un error del frontend.

-----------------------------------------
Producción / Integración

En producción o en el entorno de integración:

MONGO_URI DEBE estar configurado
El backend habilita correctamente la API
El frontend funciona sin cambios adicionales

-----------------------------------------
Conclusión

El frontend SINAPSIS está completo y funcional
No requiere modificaciones adicionales
Queda a la espera de MongoDB en backend para ambientes productivos