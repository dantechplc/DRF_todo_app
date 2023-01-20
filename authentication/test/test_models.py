from rest_framework.test import APITestCase
from authentication.models import User


class TestModel(APITestCase):

    def test_creates_user(self):
        """" test for creating a user """
        user = User.objects.create_user('dan@gmail.com', 'password123!@')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'dan@gmail.com')


    def test_creates_super_user(self):
        """" test for creating a super user """
        user = User.objects.create_superuser('super@gmail.com', 'password123!@')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email, 'super@gmail.com')

    def test_raises_error_if_email_is_not_provided(self):
        """" test raises error if email is not provided """

        self.assertRaises(ValueError, User.objects.create_user, email=None, password='password123!@')
        self.assertRaisesMessage(ValueError, "Email field is required")

    def test_raises_error_message_if_email_is_not_provided(self):
        """" test raises error message if email is not provided """
        with self.assertRaisesMessage(ValueError, "Email field is required"):
            User.objects.create_user(email='', password='password123!@')

    def test_create_super_user_with_staff_user_status(self):
        """" test raises error message if staff status is False """
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(email='super@gmail.com', password='password123!@', is_staff=False)

    def test_create_super_user_with_super_user_status(self):
        """" test raises error message if staff status is False """
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True"):
            User.objects.create_superuser(email='super@gmail.com', password='password123!@', is_superuser=False)

    def test_to_return_string_after_creating_a_user(self):
        user = User.objects.create_user('dan@gmail.com', 'password123!@')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'dan@gmail.com')
        return user

