from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status

from ..models import Author


# Test signup and login
class AuthenticationTest(TestCase):
    def setUp(self):
        testuser = User.objects.create(username="user1", password="test1")
        Author.objects.create(user=testuser, displayName="user1")
        testuser.is_active = True
        testuser.save()

    def test_sign_up_form(self):
        response = self.client.get(reverse("project:signup"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_valid(self):
        request = {"username": "user2", "password1": "test2", "password2": "test2"}

        response = self.client.post(reverse("project:signup"), request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_form(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_valid(self):
        request = {"username": "user1", "password": "test1"}

        response = self.client.post(reverse("login"), request)

        reverse("project:home")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class ProfileEditViewTest(TestCase):
    def setUp(self):
        testuser = User.objects.create(username="user1", password="test1")
        Author.objects.create(user=testuser, displayName="user1")
        self.client.force_login(testuser)
        self.author = testuser.author

    def test_edit_profile(self):
        url = reverse("project:profile_edit")

        request = {"github": "github.com", "bio": "test bio"}

        response = self.client.post(url, request)

        self.assertRedirects(
            response,
            "/project/edit/",
            status_code=status.HTTP_302_FOUND,
            target_status_code=status.HTTP_200_OK,
            fetch_redirect_response=True,
        )
