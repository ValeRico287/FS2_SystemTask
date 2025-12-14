from django.core.management.base import BaseCommand
from notifications.services import check_and_send_due_notifications


class Command(BaseCommand):
    help = 'Verifica y envía notificaciones de tareas próximas a vencer'

    def handle(self, *args, **options):
        self.stdout.write('Verificando tareas y enviando notificaciones...')
        check_and_send_due_notifications()
        self.stdout.write(self.style.SUCCESS('Proceso completado'))
