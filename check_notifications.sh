#!/bin/bash
# Script para ejecutar las notificaciones de tareas periódicamente

cd /code
python manage.py send_task_notifications
