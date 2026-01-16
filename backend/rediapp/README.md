# RedIapp – Plataforma Interna SRNI

## 1. Descripción General

**RedIapp** es una **plataforma interna** desarrollada para la **Subdirección de la Red Nacional de Información (SRNI)**, cuyo objetivo es **automatizar, centralizar y estructurar los procesos internos**, así como **consolidar la información administrativa y operativa en una base de datos central** que permita la **toma de decisiones en tiempo real**.

El sistema nace como una solución transversal para soportar procesos como:

* Automatización documental
* Gestión de actividades internas
* Centralización de información contractual y administrativa
* Preparación de datos para análisis y reportería

La automatización documental es **uno de los módulos iniciales**, pero **no representa el alcance total del aplicativo**.

---

## 2. Objetivo del Sistema

* Reducir procesos manuales repetitivos.
* Estandarizar flujos internos.
* Centralizar información crítica en una única fuente de datos.
* Permitir trazabilidad, auditoría y control.
* Facilitar la evolución hacia analítica y visualización en tiempo real.

---

## 3. Arquitectura General

RedIapp sigue una arquitectura **backend-first**, modular y extensible.

### Componentes principales:

* **Backend:** Django
* **Servidor de aplicaciones:** Gunicorn
* **Base de datos:** PostgreSQL
* **Gestión de servicios:** systemd
* **Exposición externa:** Ngrok (HTTPS)
* **Sistema operativo:** Linux (Ubuntu Server)

---

## 4. Estructura del Proyecto

```
RedIapp/
├── apps/
│   ├── accounts/
│   ├── analytics/
│   ├── dashboard/
│   ├── colaboradores/
│   └── automatizacion_documental/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
├── staticfiles/
├── templates/
├── logs/
├── manage.py
└── README.md
```

Cada módulo en `apps/` representa un dominio funcional independiente.

---

## 5. Módulos Actuales

### 5.1 Automatización Documental

Funcionalidades:

* Carga masiva de documentos en ZIP
* Carga de firma digital (PNG)
* Firma automática de documentos DOCX
* Conversión de DOCX a PDF (LibreOffice)
* Generación de ZIP con PDFs firmados
* Registro de logs del proceso en tiempo real

Este módulo opera por **sesiones de trabajo**, garantizando aislamiento y trazabilidad.

---

## 6. Base de Datos

* **Motor:** PostgreSQL
* **Base:** `srni_actividades`
* **Conexión:** local al servidor de despliegue

La base de datos es el **núcleo de la plataforma** y está diseñada para crecer hacia dominios administrativos y contractuales.

> Para desarrollo o pruebas, se puede solicitar un **dump de PostgreSQL** al administrador del sistema.

---

## 7. Despliegue

### 7.1 URL Pública

El backend se encuentra expuesto vía HTTPS mediante Ngrok:

```
https://srni-backend.ngrok.io
```

### 7.2 Puerto Interno

```
0.0.0.0:8085
```

Este puerto está reservado exclusivamente para RedIapp.

---

## 8. Servicio systemd

El backend corre como un servicio administrado por **systemd**.

### Nombre del servicio

```
srni.service
```

### Archivo del servicio

Ubicación:

```
/etc/systemd/system/srni.service
```

Configuración:

```ini
[Unit]
Description=RedIapp - Backend Django (Gunicorn)
After=network.target

[Service]
User=desarrollo
Group=desarrollo
WorkingDirectory=/home/desarrollo/RedIapp

Environment="DJANGO_SETTINGS_MODULE=config.settings"
Environment="PYTHONUNBUFFERED=1"

ExecStart=/home/desarrollo/RedIapp/venv/bin/gunicorn \
    --workers 3 \
    --bind 0.0.0.0:8085 \
    --timeout 120 \
    --access-logfile /home/desarrollo/RedIapp/logs/access.log \
    --error-logfile /home/desarrollo/RedIapp/logs/error.log \
    config.wsgi:application

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 9. Logs y Monitoreo

### Logs de la aplicación

Ubicación:

```
/home/desarrollo/RedIapp/logs/
```

* `access.log` – solicitudes HTTP
* `error.log` – errores del backend

Visualización en tiempo real:

```bash
tail -f /home/desarrollo/RedIapp/logs/error.log
tail -f /home/desarrollo/RedIapp/logs/access.log
```

### Logs del servicio

```bash
sudo systemctl status srni.service
sudo journalctl -u srni.service -f
```

---

## 10. Operación Básica

Reiniciar servicio:

```bash
sudo systemctl restart srni.service
```

Detener servicio:

```bash
sudo systemctl stop srni.service
```

Verificar puerto:

```bash
sudo ss -tulnp | grep 8085
```

---

## 11. Seguridad

* Acceso externo únicamente por HTTPS.
* Autenticación basada en usuarios Django.
* Protección CSRF habilitada.
* Endpoints críticos controlados explícitamente.
* No se exponen puertos directamente a internet.

---

## 12. Estado del Proyecto

RedIapp se encuentra en **fase activa de evolución**.

* Automatización documental: operativo.
* Nuevos módulos administrativos: en diseño y expansión.
* Enfoque principal: **plataforma interna de apoyo a decisiones SRNI**.

---

## 13. Contacto Técnico

Para temas de:

* Acceso
* Dumps de base de datos
* Arquitectura
* Nuevos módulos

Contactar al **administrador técnico del sistema**.

