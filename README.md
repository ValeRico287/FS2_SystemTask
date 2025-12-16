#  Sistema de Gestión de Tareas Colaborativas

[![Django](https://img.shields.io/badge/Django-5.2.2-green. svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12.4-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

Sistema web colaborativo de gestión de tareas desarrollado con Django y PostgreSQL, diseñado para equipos de trabajo que necesitan organizar, asignar y dar seguimiento a tareas con notificaciones automáticas por correo electrónico.

##  Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso del Sistema](#-uso-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Sistema de Roles](#-sistema-de-roles)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

##  Características Principales

###  Sistema de Autenticación y Roles
- **Tres niveles de acceso**:  Admin, Team Lead, y User
- Autenticación basada en email
- Gestión de permisos por rol
- Sistema de equipos con líderes asignables

###  Gestión de Tareas
- Crear, editar y eliminar tareas
- Asignación múltiple de usuarios a una misma tarea
- Estados de tareas:  To Do, In Progress, Review, Done
- Prioridades: Low, Medium, High, Urgent
- Fechas de vencimiento con selector de fecha/hora
- Sistema de comentarios por tarea
- Identificadores UUID únicos para cada tarea

###  Gestión de Equipos
- Creación de equipos por administradores
- Asignación de líderes de equipo
- Agregar/remover miembros del equipo
- Vista detallada de equipos con todas sus tareas

### Sistema de Notificaciones por Email
- Notificación al crear una tarea nueva
- Recordatorio 24 horas antes del vencimiento
- Recordatorio urgente 1 hora antes del vencimiento
- Notificación cuando una tarea se vence
- Ejecución automática mediante cron jobs

###  Dashboard Interactivo
- Estadísticas en tiempo real de tareas
- Filtrado por estado, prioridad y equipo
- Vista de tareas asignadas personalmente
- Indicadores visuales de tareas próximas a vencer

##  Tecnologías Utilizadas

### Backend
- **Django 5.2.2** - Framework web de Python
- **PostgreSQL** - Base de datos relacional
- **Python 3.12.4** - Lenguaje de programación

### Frontend
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Iconografía
- **Flatpickr** - Selector de fechas
- **Crispy Forms** - Formularios con Bootstrap

### DevOps
- **Docker & Docker Compose** - Contenedorización
- **Gunicorn** - Servidor WSGI para producción
- **Cron** - Programación de tareas automáticas

### Librerías Python Principales
```
Django==5.2.2
psycopg2-binary==2.9.10
django-crispy-forms==2.3
crispy-bootstrap5==2025.6
python-decouple==3.8
Pillow==11.2.1
```

## Requisitos Previos

- Docker y Docker Compose instalados
- Puerto 8000 disponible para la aplicación web
- Puerto 5432 disponible para PostgreSQL
- Cuenta de Gmail con contraseña de aplicación (para notificaciones)

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ValeRico287/FS2_SystemTask. git
cd FS2_SystemTask
```

### 2. Configurar Variables de Entorno

Copia el archivo de ejemplo y edita las variables: 

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```env
# Django
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpass
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=tu-email@gmail.com
```

### 3. Construir y Levantar los Contenedores

```bash
docker compose up --build -d
```

### 4. Aplicar Migraciones

```bash
docker compose exec web python manage. py makemigrations
docker compose exec web python manage.py migrate
```

### 5. Crear Superusuario

```bash
docker compose exec web python manage. py createsuperuser
```

Proporciona: 
- Email
- Nombre
- Contraseña

### 6. Configurar Notificaciones Automáticas (Opcional)

```bash
# Instalar cron en el contenedor
docker compose exec web apt-get update
docker compose exec web apt-get install -y cron

# Agregar el cron job
docker compose exec web crontab /code/crontab.txt

# Iniciar el servicio cron
docker compose exec web service cron start
```

### 7. Acceder al Sistema

Abre tu navegador en:  **http://localhost:8000**

## Configuración

### Configuración de Email para Gmail

1. Ve a tu cuenta de Google
2. Habilita la verificación en dos pasos
3. Genera una contraseña de aplicación en:  https://myaccount.google.com/apppasswords
4. Usa esa contraseña en `EMAIL_HOST_PASSWORD` del archivo `.env`

### Ejecutar Notificaciones Manualmente

Para probar el sistema de notificaciones:

```bash
docker compose exec web python manage.py send_task_notifications
```

## Uso del Sistema

### Como Administrador (Admin)

1. **Crear Equipos**
   - Navega a "Equipos" → "Nuevo Equipo"
   - Completa nombre y descripción
   - Asigna un líder de equipo

2. **Gestionar Líderes**
   - Accede al detalle del equipo
   - Click en "Asignar/Cambiar Líder"
   - Selecciona el nuevo líder

3. **Supervisar Todo el Sistema**
   - Vista completa de todos los equipos
   - Acceso a todas las tareas
   - Gestión completa de usuarios

### Como Líder de Equipo (Team Lead)

1. **Gestionar Miembros**
   - Agregar usuarios al equipo
   - Remover miembros (excepto el líder)
   - Ver listado completo del equipo

2. **Crear y Asignar Tareas**
   - Click en "Nueva Tarea"
   - Completa título, descripción y fecha de vencimiento
   - Selecciona prioridad y estado
   - Asigna a múltiples usuarios (mantén Ctrl/Cmd)

3. **Editar Tareas del Equipo**
   - Modificar cualquier tarea del equipo
   - Reasignar usuarios
   - Cambiar prioridades y fechas

### Como Usuario (User)

1. **Ver Tareas Asignadas**
   - Dashboard con todas tus tareas
   - Filtros por estado y prioridad
   - Vista de "Mis Tareas"

2. **Actualizar Estado de Tareas**
   - Accede al detalle de la tarea
   - Click en "Cambiar Estado"
   - Selecciona:  To Do → In Progress → Review → Done

3. **Comentar en Tareas**
   - Agrega comentarios en las tareas
   - Colabora con el equipo

## 📁 Estructura del Proyecto

```
FS2_SystemTask/
├── accounts/              # App de autenticación y usuarios
│   ├── models.py         # Modelo de usuario personalizado
│   ├── views.py          # Vistas de registro/login
│   └── forms.py          # Formularios de autenticación
├── tasks/                # App de gestión de tareas
│   ├── models.py         # Modelos Task y Comment
│   ├── views.py          # Vistas CRUD de tareas
│   └── forms.py          # Formularios de tareas
├── teams/                # App de gestión de equipos
│   ├── models.py         # Modelo Team
│   ├── views.py          # Vistas de equipos
│   └── forms. py          # Formularios de equipos
├── notifications/        # App de notificaciones
│   └── management/
│       └── commands/
│           └── send_task_notifications.py
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── registration/
│   ├── tasks/
│   └── teams/
├── static/               # Archivos estáticos
│   ├── css/
│   └── js/
├── config/               # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml    # Configuración Docker
├── Dockerfile            # Imagen Docker
├── requirements.txt      # Dependencias Python
├── .env.example          # Variables de entorno ejemplo
└── manage.py             # CLI de Django
```

## Sistema de Roles

| Rol | Permisos |
|-----|----------|
| **Admin** | • Crear y gestionar equipos<br>• Asignar/cambiar líderes<br>• Acceso total al sistema<br>• Ver todas las tareas y equipos |
| **Team Lead** | • Agregar/remover miembros del equipo<br>• Crear, editar y eliminar tareas del equipo<br>• Asignar tareas a miembros<br>• Ver tareas del equipo |
| **User** | • Ver tareas asignadas<br>• Cambiar estado de sus tareas<br>• Comentar en tareas<br>• Ver información del equipo |

## Comandos Útiles

```bash
# Ver logs de la aplicación
docker compose logs -f web

# Ver logs de PostgreSQL
docker compose logs -f db

# Detener los contenedores
docker compose down

# Reiniciar los contenedores
docker compose restart

# Ejecutar shell de Django
docker compose exec web python manage.py shell

# Crear migraciones
docker compose exec web python manage.py makemigrations

# Aplicar migraciones
docker compose exec web python manage.py migrate

# Crear datos de prueba
docker compose exec web python manage.py loaddata fixtures/initial_data.json
```

## Solución de Problemas

### Las notificaciones no se envían

1. Verifica la configuración de email en `.env`
2. Prueba el envío manual:
   ```bash
   docker compose exec web python manage.py send_task_notifications
   ```
3. Verifica que cron esté activo: 
   ```bash
   docker compose exec web service cron status
   ```

### Error de conexión a la base de datos

1. Verifica que PostgreSQL esté corriendo:
   ```bash
   docker compose ps
   ```
2. Revisa las credenciales en `.env`
3. Reinicia los contenedores:
   ```bash
   docker compose restart
   ```

### No se cargan los estilos

1. Ejecuta collectstatic:
   ```bash
   docker compose exec web python manage. py collectstatic --noinput
   ```


## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor

**ValeRico287**

- GitHub: [@ValeRico287](https://github.com/ValeRico287)
- Repositorio: [FS2_SystemTask](https://github.com/ValeRico287/FS2_SystemTask)

## Agradecimientos

- Django Documentation
- Bootstrap Team
- PostgreSQL Community
- Docker Community

---
