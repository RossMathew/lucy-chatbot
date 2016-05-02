from django.test import TestCase
from .models import MyUser


class MyUserTestCase(TestCase):
    def setup(self):
        MyUser.objects.create_user(
        email="rrmerugu@gmail.com",
        password="welcome123",
        first_name="Ravi"
        )
        MyUser.objects.create_user(
        email="ravi@rsquarelabs.com",
        password="welcome123",
        first_name="R2 Labs"
        )
        MyUser.objects.create_user(
        email="raviraja.merugu@gmail.com",
        password="welcome123",
        first_name="Raja"
        )

    def test_user_registration(self):

        ravi = MyUser.objects.get(first_name="ravi")
        self.assertEqual(ravi.email, 'rrmerugu@gmail.com')
