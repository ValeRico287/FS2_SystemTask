from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import timedelta
from tasks.models import Task
from notifications.models import Notification, TaskNotificationTracker


def send_task_notification_email(user, task, notification_type):
    """Envía un email de notificación a un usuario sobre una tarea con diseño HTML"""
    
    # Configuración de colores y badges según tipo de notificación
    notification_config = {
        'task_created': {
            'subject': f'✨ Nueva tarea asignada: {task.title}',
            'message': 'Se te ha asignado una nueva tarea. Por favor, revisa los detalles y comienza a trabajar en ella.',
            'badge_color': '#667eea',
            'display': '📋 Nueva Tarea'
        },
        'task_due_24h': {
            'subject': f'⏰ Recordatorio: Tarea vence en 24 horas - {task.title}',
            'message': 'Esta tarea vencerá en las próximas 24 horas. Asegúrate de completarla a tiempo.',
            'badge_color': '#fbbf24',
            'display': '⏰ Vence en 24 Horas'
        },
        'task_due_1h': {
            'subject': f'🚨 ¡URGENTE! Tarea vence en 1 hora - {task.title}',
            'message': '¡Atención! Esta tarea vencerá en 1 hora. Por favor, complétala lo antes posible.',
            'badge_color': '#f59e0b',
            'display': '🚨 Vence en 1 Hora'
        },
        'task_overdue': {
            'subject': f'❌ Tarea vencida: {task.title}',
            'message': 'Esta tarea ha vencido. Por favor, actualiza su estado o contacta al líder del equipo.',
            'badge_color': '#ef4444',
            'display': '❌ Tarea Vencida'
        },
    }
    
    config = notification_config.get(notification_type, notification_config['task_created'])
    
    # Colores según prioridad
    priority_colors = {
        'urgent': '#dc2626',
        'high': '#f59e0b',
        'medium': '#3b82f6',
        'low': '#10b981'
    }
    
    # Contexto para el template
    context = {
        'subject': config['subject'],
        'user_name': user.name,
        'message': config['message'],
        'notification_type_display': config['display'],
        'badge_color': config['badge_color'],
        'task_title': task.title,
        'task_description': task.description[:200] if task.description else 'Sin descripción',
        'task_priority': task.get_priority_display(),
        'task_due_date': task.due_date.strftime('%d/%m/%Y %H:%M') if task.due_date else 'Sin fecha',
        'task_team': task.team.name,
        'task_uuid': str(task.uuid),  # UUID único de la tarea
        'task_url': f'{settings.DEFAULT_FROM_EMAIL}/task/{task.pk}/',  # URL de la tarea
        'priority_color': priority_colors.get(task.priority, '#3b82f6'),
    }
    
    # Renderizar template HTML
    html_content = render_to_string('emails/task_notification.html', context)
    
    # Crear email con HTML
    email = EmailMultiAlternatives(
        subject=config['subject'],
        body=config['message'],  # Texto plano como fallback
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error enviando email a {user.email}: {str(e)}")
        return False


def notify_task_created(task):
    """Envía notificaciones cuando se crea una tarea"""
    # Crear o obtener el tracker
    tracker, created = TaskNotificationTracker.objects.get_or_create(task=task)
    
    if tracker.created_notification_sent:
        return
    
    # Notificar a todos los usuarios asignados
    for user in task.assigned_to.all():
        # Crear notificación en BD
        notification = Notification.objects.create(
            user=user,
            task=task,
            message=f'Se te ha asignado la tarea: {task.title}',
            notification_type='task_created'
        )
        
        # Enviar email
        email_sent = send_task_notification_email(user, task, 'task_created')
        notification.email_sent = email_sent
        notification.save()
    
    # Marcar como enviada
    tracker.created_notification_sent = True
    tracker.save()


def check_and_send_due_notifications():
    """Verifica y envía notificaciones de tareas próximas a vencer o vencidas"""
    now = timezone.now()
    
    # Obtener tareas pendientes con fecha de vencimiento
    pending_tasks = Task.objects.filter(
        status__in=['to_do', 'in_progress', 'review'],
        due_date__isnull=False
    ).select_related('team').prefetch_related('assigned_to')
    
    for task in pending_tasks:
        tracker, created = TaskNotificationTracker.objects.get_or_create(task=task)
        
        time_until_due = task.due_date - now
        
        # Tarea vencida
        if time_until_due.total_seconds() < 0 and not tracker.overdue_notification_sent:
            for user in task.assigned_to.all():
                notification = Notification.objects.create(
                    user=user,
                    task=task,
                    message=f'La tarea "{task.title}" ha vencido.',
                    notification_type='task_overdue'
                )
                email_sent = send_task_notification_email(user, task, 'task_overdue')
                notification.email_sent = email_sent
                notification.save()
            
            tracker.overdue_notification_sent = True
            tracker.save()
        
        # Vence en 1 hora
        elif 0 <= time_until_due.total_seconds() <= 3600 and not tracker.due_1h_notification_sent:
            for user in task.assigned_to.all():
                notification = Notification.objects.create(
                    user=user,
                    task=task,
                    message=f'La tarea "{task.title}" vence en 1 hora.',
                    notification_type='task_due_1h'
                )
                email_sent = send_task_notification_email(user, task, 'task_due_1h')
                notification.email_sent = email_sent
                notification.save()
            
            tracker.due_1h_notification_sent = True
            tracker.save()
        
        # Vence en 24 horas
        elif 3600 < time_until_due.total_seconds() <= 86400 and not tracker.due_24h_notification_sent:
            for user in task.assigned_to.all():
                notification = Notification.objects.create(
                    user=user,
                    task=task,
                    message=f'La tarea "{task.title}" vence en 24 horas.',
                    notification_type='task_due_24h'
                )
                email_sent = send_task_notification_email(user, task, 'task_due_24h')
                notification.email_sent = email_sent
                notification.save()
            
            tracker.due_24h_notification_sent = True
            tracker.save()
