#!/bin/bash
# Script para aplicar todos los cambios del backend

echo "====================================="
echo "APLICANDO CAMBIOS DEL BACKEND"
echo "====================================="

echo ""
echo "1. Generando migraciones..."
docker compose exec web python manage.py makemigrations

echo ""
echo "2. Aplicando migraciones..."
docker compose exec web python manage.py migrate

echo ""
echo "3. Creando estructura de carpetas para notificaciones..."
docker compose exec web mkdir -p notifications/management/commands

echo ""
echo "====================================="
echo "CONFIGURACIÓN COMPLETADA"
echo "====================================="

echo ""
echo "Pasos siguientes:"
echo ""
echo "1. Crear un superusuario:"
echo "   docker compose exec web python manage.py createsuperuser"
echo ""
echo "2. Probar el sistema de notificaciones:"
echo "   docker compose exec web python manage.py send_task_notifications"
echo ""
echo "3. Configurar cron para notificaciones automáticas:"
echo "   docker compose exec web apt-get update && apt-get install -y cron"
echo "   docker compose exec web crontab /code/crontab.txt"
echo "   docker compose exec web service cron start"
echo ""
echo "4. Acceder al sistema en: http://localhost:8000"
echo ""
echo "Para más información, consultar BACKEND_README.md"
