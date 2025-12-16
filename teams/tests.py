from django.test import TestCase
from accounts.models import User
from teams.models import Team, TeamMember


# TESTS UNITARIOS
class TeamModelTest(TestCase):

    def test_create_team(self):
        team = Team.objects.create(name="Backend Team")
        self.assertEqual(team.name, "Backend Team")

    def test_team_with_lead(self):
        lead = User.objects.create(
            name="Lead",
            email="lead@test.com",
            role="team_lead",
            password="123"
        )

        team = Team.objects.create(
            name="Dev Team",
            team_lead=lead
        )

        self.assertEqual(team.team_lead.email, "lead@test.com")


# TESTS DE INTEGRACIÓN

class TeamIntegrationTest(TestCase):

    def test_add_user_to_team(self):
        user = User.objects.create(
            name="User",
            email="user@test.com",
            role="user",
            password="123"
        )

        team = Team.objects.create(name="QA Team")

        TeamMember.objects.create(team=team, user=user)

        self.assertEqual(team.members.count(), 1)

    def test_no_duplicate_team_member(self):
        user = User.objects.create(
            name="User2",
            email="user2@test.com",
            role="user",
            password="123"
        )

        team = Team.objects.create(name="Design Team")

        TeamMember.objects.create(team=team, user=user)

        with self.assertRaises(Exception):
            TeamMember.objects.create(team=team, user=user)
