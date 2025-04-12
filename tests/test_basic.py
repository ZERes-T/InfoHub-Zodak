from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from feedback.models import Feedback
from games.models import Game
from django.urls import reverse

User = get_user_model()

class BasicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@example.com")

    def test_register_and_login(self):
        response = self.client.post("/accounts/signup/", {
            "username": "newuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "email": "new@example.com"
        })
        self.assertEqual(response.status_code, 302)

        login = self.client.login(username="newuser", password="testpass123")
        self.assertTrue(login)

    def test_feedback_submission(self):
        response = self.client.post("/feedback/", {
            "name": "Test User",
            "email": "user@example.com",
            "message": "Great project!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), 1)

    def test_game_creation_and_view(self):
        game = Game.objects.create(title="Test Game", description="Awesome", size="1 GB", os="Windows")
        response = self.client.get("/")
        self.assertContains(response, "Test Game")

    def test_profile_view_requires_login(self):
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 302)  # Redirect to login

        self.client.login(username="testuser", password="testpass")
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)