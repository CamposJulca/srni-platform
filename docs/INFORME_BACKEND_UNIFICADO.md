
# 📄 Informe técnico

## Unificación y contenedorización del backend – SRNI Platform

**Fecha:** enero 2026
**Rama base:** `develop`
**Responsable de arquitectura e infraestructura:** Daniel
**Responsable de desarrollo fullstack (continuidad):** Jorge

---

## 1. Objetivo del trabajo realizado

El objetivo de esta fase fue  **consolidar un único backend funcional** , eliminando duplicidades históricas, unificando dominios de negocio y garantizando:

* Arquitectura coherente basada en dominios
* Backend **100% dockerizado**
* Conexión estable a servicios de datos (PostgreSQL, MongoDB, MinIO, Elastic)
* Base sólida para desarrollo fullstack continuo

Este objetivo  **ya fue alcanzado y validado** .

---

## 2. Resultado final (estado actual del sistema)

### 2.1 Backend unificado

El backend quedó centralizado en:

```
backend/rni_web/
```

Con una estructura por  **dominios funcionales** :

```
src/apps/
├── accounts
├── analytics
├── automatizacion_documental
├── colaboradores
├── dashboard
├── nlquery
```

Cada dominio contiene:

* `models.py`
* `views.py`
* `urls.py` / `urls_api.py`
* `admin.py`
* `services/` (cuando aplica)
* `migrations/`

No existen imports legacy ni dependencias cruzadas indebidas.

---

### 2.2 Backend dockerizado (estado estable)

El backend corre  **exclusivamente en contenedor** , con:

* `Dockerfile`
* `docker-compose.yml`
* `entrypoint.sh`

Características clave:

* Espera activa a PostgreSQL (`pg_isready`)
* Migraciones automáticas al levantar el contenedor
* Variables de entorno desacopladas (`.env`)
* Red compartida con el stack de datos (`data_stack_net`)

El contenedor productivo es:

```
rni_backend
```

---

### 2.3 Stack de datos

El backend se integra con servicios **ya operativos** vía Docker:

* PostgreSQL (`postgres_local`)
* MongoDB (`mongo_local`)
* MinIO (`minio_local`)
* Elasticsearch + Kibana

Todos los servicios comparten la red:

```
data_stack_net
```

No se requiere configuración adicional para desarrollo.

---

## 3. Estado de migraciones

* Migraciones **base** aplicadas correctamente:
  * `admin`
  * `auth`
  * `contenttypes`
  * `sessions`
  * `core`
* Los dominios nuevos (`apps/*`)  **no tienen migraciones aún** , lo cual es correcto en esta fase.

👉  **Cualquier cambio de modelo futuro deberá generar sus propias migraciones** .

---

## 4. Qué debe hacer Jorge a partir de ahora

### 4.1 Rol esperado

Jorge continúa como  **desarrollador fullstack** , responsable de:

* Lógica de negocio
* APIs REST
* Vistas / templates
* Integración frontend–backend
* Creación de migraciones nuevas por dominio

---

### 4.2 Flujo de trabajo recomendado

1. Trabajar **siempre sobre `develop`**
2. Crear ramas por feature:
   ```
   feature/dashboard-kpis
   feature/automatizacion-masiva
   ```
3. No modificar:
   * Dockerfile
   * docker-compose del backend
   * entrypoint.sh
   * infraestructura base

---

### 4.3 Cómo levantar el entorno (resumen)

```bash
# Stack de datos
docker compose -f infra/docker-compose.yml up -d

# Backend
docker compose -f backend/rni_web/docker-compose.yml up -d --build
```

El backend queda disponible en:

```
http://localhost:8000
```

---

## 5. Decisiones arquitectónicas importantes

* ❌ No microservicios en esta fase
* ✅ Backend monolítico modular por dominios
* ✅ Separación clara: infraestructura / backend / frontend
* ✅ Docker como única forma de ejecución
* ✅ Base preparada para escalamiento futuro

---

## 6. Límites de esta fase (importante)

Este informe **cierra oficialmente** la fase de:

> **Unificación + contenedorización del backend**

No incluye:

* Optimización de queries
* Seguridad avanzada
* Autenticación robusta
* Despliegue productivo
* Observabilidad

Eso corresponde a  **fases posteriores** .

---

## 7. Estado final

✔ Backend único
✔ Backend funcional
✔ Backend dockerizado
✔ Rama `develop` estable
✔ Infraestructura validada

