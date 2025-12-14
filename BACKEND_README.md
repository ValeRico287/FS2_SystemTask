# Sistema de Gestión de Tareas Colaborativas

## Características Implementadas

### Sistema de Roles y Permisos

#### Admin
- Crear equipos y asignar líderes
- Cambiar líderes de equipos existentes
- Ver todos los equipos y tareas del sistema
- Acceso total al sistema

#### Team Lead
- Agregar y eliminar miembros de su equipo
- Crear tareas y asignarlas a múltiples usuarios
- Editar y eliminar tareas de su equipo
- Ver tareas de su equipo

#### User
- Ver tareas asignadas
- Cambiar el estado de sus tareas (To Do, In Progress, Review, Done)
- Ver información de su equipo

### Sistema de Notificaciones por Email

El sistema envía notificaciones automáticas por email en los siguientes casos:
- **Al crear una tarea**: Notifica a todos los usuarios asignados
- **24 horas antes de vencer**: Recordatorio
- **1 hora antes de vencer**: Recordatorio urgente
- **Cuando se vence**: Notificación de tarea vencida

### Asignación Múltiple de Usuarios

Las tareas pueden ser asignadas a múltiples usuarios simultáneamente.

## Instalación y Configuración

### 1. Aplicar Migraciones

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### 2. Crear Superusuario

```bash
docker compose exec web python manage.py createsuperuser
```

### 3. Configurar Notificaciones Automáticas

Para ejecutar las notificaciones automáticamente cada 10 minutos:

```bash
# Instalar cron en el contenedor (si no está)
docker compose exec web apt-get update
docker compose exec web apt-get install -y cron

# Agregar el cron job
docker compose exec web crontab /code/crontab.txt

# Iniciar el servicio cron
docker compose exec web service cron start
```

### 4. Ejecutar Notificaciones Manualmente

Si quieres probar el sistema de notificaciones:

```bash
docker compose exec web python manage.py send_task_notifications
```

## Uso del Sistema

### Como Admin

1. **Crear un equipo**:
   - Ir a "Equipos" → "Nuevo Equipo"
   - Llenar nombre, descripción y seleccionar líder

2. **Asignar/Cambiar líder**:
   - Ir al detalle del equipo
   - Click en "Asignar/Cambiar Líder"

### Como Team Lead

1. **Agregar miembros al equipo**:
   - Ir al detalle del equipo
   - Click en "Agregar Miembro"
   - Seleccionar usuario de la lista

2. **Crear tarea**:
   - Click en "Nueva Tarea"
   - Llenar información
   - Seleccionar múltiples usuarios manteniendo Ctrl (Cmd en Mac)

3. **Eliminar miembros**:
   - En el detalle del equipo, click en X junto al usuario

### Como User

1. **Ver mis tareas**:
   - Dashboard muestra todas tus tareas
   - "Mis Tareas" muestra solo las asignadas a ti

2. **Cambiar estado de tarea**:
   - Entrar al detalle de la tarea
   - Click en "Cambiar Estado"
   - Seleccionar nuevo estado

## Configuración de Email

El sistema está configurado para usar Gmail con las siguientes credenciales:
- Email: correoscrear8@gmail.com
- App Password: jopu kbip yvym gevc

Para cambiar estas credenciales, editar `config/settings.py`:

```python
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-app-password'
```

## Estructura de URLs

### Equipos
- `/teams/` - Lista de equipos
- `/teams/new/` - Crear equipo (Admin)
- `/teams/<id>/` - Detalle del equipo
- `/teams/<id>/assign-lead/` - Asignar líder (Admin)
- `/teams/<id>/add-member/` - Agregar miembro (Team Lead)
- `/teams/<id>/remove-member/<user_id>/` - Eliminar miembro (Team Lead)

### Tareas
- `/` - Dashboard
- `/mis-tareas/` - Mis tareas
- `/task/new/` - Crear tarea (Team Lead/Admin)
- `/task/<id>/` - Detalle de tarea
- `/task/<id>/edit/` - Editar tarea (Team Lead/Admin)
- `/task/<id>/delete/` - Eliminar tarea (Team Lead/Admin)
- `/task/<id>/update-status/` - Cambiar estado (User asignado)

## Solución de Problemas

### Las notificaciones no se envían

1. Verificar que el email esté configurado correctamente
2. Probar envío manual:
   ```bash
   docker compose exec web python manage.py send_task_notifications
   ```
3. Verificar que cron esté corriendo:
   ```bash
   docker compose exec web service cron status
   ```

### Error al asignar usuarios

Asegúrate de que:
- Los usuarios sean miembros del equipo
- Estés manteniendo Ctrl al seleccionar múltiples usuarios
- El equipo tenga miembros agregados

## Notas Importantes

- Las fechas de vencimiento deben incluir hora para que las notificaciones funcionen correctamente
- Un usuario no puede eliminar al líder del equipo
- Solo Team Leads y Admins pueden crear tareas
- Los usuarios solo pueden cambiar el estado de tareas asignadas a ellos
