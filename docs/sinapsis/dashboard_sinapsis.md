# Dashboard SINAPSIS  
**Módulo analítico de proyectos tecnológicos**

---

## 📌 Contexto

SINAPSIS es una fuente institucional que concentra información sobre el **portafolio de proyectos tecnológicos** de la Red Nacional de Información.

Este módulo implementa un **dashboard analítico** que permite visualizar, explorar y analizar dicho portafolio de forma estructurada, reproducible y desacoplada de la fuente original.

---

## 🎯 Objetivo del módulo

- Centralizar la información de proyectos SINAPSIS
- Proveer visualización analítica en tiempo real
- Facilitar toma de decisiones estratégicas y operativas
- Servir como base para analítica institucional futura

---

## 🧱 Arquitectura del módulo

```text
SINAPSIS (externo)
        ↓
Backend Django (API /sinapsis)
        ↓
Normalización / Servicios
        ↓
Frontend React (Dashboard)
````

---

## ⚙️ Componentes técnicos

### Backend

* Django + Django REST Framework
* Servicios desacoplados (`repositories`, `services`, `views`)
* Endpoint principal:

  ```
  GET /api/sinapsis/projects/
  ```

### Frontend

* React + Vite
* Librería de visualización: Recharts
* Consumo vía `fetch` desde API institucional

---

## 📊 Visualizaciones implementadas

### 1️⃣ Proyectos por estado

Gráfica de barras que muestra la distribución de proyectos según su estado:

* Active
* Planificado
* Planning
* On Hold

**Propósito:** visión operativa del portafolio.

---

### 2️⃣ Proyectos por ciclo de vida

Gráfica circular (pie chart) con los ciclos:

* Concept
* Development
* Maintenance
* Production
* Retirement
* No definido

**Propósito:** madurez tecnológica del portafolio.

---

### 3️⃣ Proyectos por nivel de riesgo

Gráfica de barras:

* High
* Medium
* Low
* No definido

**Propósito:** identificación temprana de riesgos institucionales.

---

### 4️⃣ Tabla detallada de proyectos

Vista tabular con:

* Nombre
* Estado
* Ciclo de vida
* Nivel de riesgo
* Tipo de iniciativa

**Propósito:** exploración detallada y trazabilidad.

---

## 🧪 Validación

### API

```bash
curl http://localhost:8000/api/sinapsis/projects/
```

### Dashboard

```
http://localhost:5173
```

---

## 🧠 Decisiones de diseño

* **Desacoplamiento total** entre fuente y visualización
* **Normalización en backend**, no en frontend
* **Visualización reactiva**, sin persistencia en cliente
* Preparado para:

  * Filtros dinámicos
  * Series temporales
  * Exportación de datos
  * Autenticación futura

---

## 📌 Evolución futura

* Filtros por dominio tecnológico
* KPIs institucionales
* Exportación CSV / PDF
* Integración con Elasticsearch
* Dashboards comparativos históricos

---

## 👤 Responsable técnico

**Daniel Campos**
Arquitectura · Analítica · Integración de sistemas

