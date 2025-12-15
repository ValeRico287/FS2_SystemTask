from django.core.management.base import BaseCommand
from tasks.models import Task
import uuid


class Command(BaseCommand):
    help = 'Genera UUIDs para todas las tareas que no tienen uno'

    def handle(self, *args, **options):
        tasks_without_uuid = Task.objects.filter(uuid__isnull=True)
        count = tasks_without_uuid.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('Todas las tareas ya tienen UUID'))
            return
        
        self.stdout.write(f'Generando UUIDs para {count} tareas...')
        
        for task in tasks_without_uuid:
            task.uuid = uuid.uuid4()
            task.save()
        
        self.stdout.write(self.style.SUCCESS(f'UUIDs generados exitosamente para {count} tareas'))
