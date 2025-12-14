# Configuración de Variables de Entorno

Este proyecto utiliza archivos `.env` para manejar información sensible y configuraciones del entorno.

## Archivos

- **`.env`**: Contiene las variables de entorno reales (NO debe subirse a Git)
- **`.env.example`**: Plantilla con variables de ejemplo para nuevos desarrolladores

## Variables de Entorno

### Django Settings
- `SECRET_KEY`: Clave secreta de Django (generarla con `django-admin startproject`)
- `DEBUG`: Modo debug (True/False)
- `ALLOWED_HOSTS`: Hosts permitidos separados por coma

### Database Configuration
- `POSTGRES_DB`: Nombre de la base de datos
- `POSTGRES_USER`: Usuario de PostgreSQL
- `POSTGRES_PASSWORD`: Contraseña de PostgreSQL
- `POSTGRES_HOST`: Host de la base de datos (por defecto: db)
- `POSTGRES_PORT`: Puerto de PostgreSQL (por defecto: 5432)

### Email Configuration
- `EMAIL_HOST`: Servidor SMTP (por defecto: smtp.gmail.com)
- `EMAIL_PORT`: Puerto SMTP (por defecto: 587)
- `EMAIL_USE_TLS`: Usar TLS (True/False)
- `EMAIL_HOST_USER`: Correo electrónico para envío
- `EMAIL_HOST_PASSWORD`: Contraseña de aplicación de Gmail
- `DEFAULT_FROM_EMAIL`: Correo remitente por defecto

## Configuración Inicial

1. Copia el archivo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edita `.env` con tus valores reales:
   ```bash
   nano .env
   ```

3. Para Gmail, genera una contraseña de aplicación:
   - Ve a: https://myaccount.google.com/apppasswords
   - Genera una nueva contraseña de aplicación
   - Úsala en `EMAIL_HOST_PASSWORD`

## Seguridad

⚠️ **IMPORTANTE**: 
- Nunca subas el archivo `.env` a Git
- El archivo `.env` está en `.gitignore` por defecto
- Comparte credenciales de forma segura (nunca por email/chat público)
