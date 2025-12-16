from django.test import TestCase
from accounts.models import User
from teams.models import Team
from tasks.models import Task

# Crear tarea.
class TaskModelTest(TestCase):

    def test_create_task(self):
        team = Team.objects.create(name="Mobile Team")

        task = Task.objects.create(
            team=team,
            title="Create Login",
            status="to_do",
            priority="high"
        )

        self.assertEqual(task.title, "Create Login")

#Tarea pertenece a un equipo
class TaskIntegrationTest(TestCase):

    def test_task_belongs_to_team(self):
        team = Team.objects.create(name="Infra Team")

        task = Task.objects.create(
            team=team,
            title="Deploy App",
            status="to_do",
            priority="urgent"
        )

        self.assertEqual(task.team.name, "Infra Team")

#Filtrar tareas por prioridad
    def test_filter_tasks_by_priority(self):
        team = Team.objects.create(name="Security Team")

        Task.objects.create(
            team=team,
            title="Low Task",
            status="to_do",
            priority="low"
        )

        Task.objects.create(
            team=team,
            title="High Task",
            status="to_do",
            priority="high"
        )

        high_tasks = Task.objects.filter(priority="high")
        self.assertEqual(high_tasks.count(), 1)
