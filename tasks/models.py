from django.db import models
from django.conf import settings
from teams.models import Team
import uuid


class Task(models.Model):

    STATUS_CHOICES = [
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # UUID para identificador único universal (útil para APIs, compartir tareas, tracking)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_tasks', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['created_at']
