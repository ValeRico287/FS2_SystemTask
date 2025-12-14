from django.db import models
from django.conf import settings
from accounts.models import User

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_teams')
    team_lead = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='led_teams'
    )
    members = models.ManyToManyField(User, through='TeamMembership', related_name='teams')

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')