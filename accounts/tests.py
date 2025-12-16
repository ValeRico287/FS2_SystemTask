from django.test import TestCase
from accounts.models import User
#Test unitarios 

#Crear usuario
class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create(
            name="Valeria",
            email="valeria@test.com",
            role="user",
            password="123456"
        )

        self.assertEqual(user.name, "Valeria")
        self.assertEqual(user.email, "valeria@test.com")
        self.assertEqual(user.role, "user")


#Email único
    def test_unique_email(self):
        User.objects.create(
            name="User1",
            email="unique@test.com",
            role="user",
            password="123"
        )

        with self.assertRaises(Exception):
            User.objects.create(
                name="User2",
                email="unique@test.com",
                role="user",
                password="123"
            )


#Rol válido
    def test_user_role_is_valid(self):
        user = User.objects.create(
            name="Admin",
            email="admin@test.com",
            role="admin",
            password="123"
        )

        self.assertIn(user.role, ["admin", "user", "team_lead"])
