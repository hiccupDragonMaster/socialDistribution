from django.contrib.auth.models import User
from django.urls import reverse

import uuid

from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Author


class FollowersAPITest(APITestCase):
    url_name = "project:get_followers"

    @classmethod
    def setUpTestData(cls):
        for name in ["Alice", "Bob", "Carl"]:
            user = User.objects.create(username=name, password="testpassword1")
            Author.objects.create(user=user, displayName=name)

    def setUp(self):
        for i, a1 in enumerate(Author.objects.all()):
            for a2 in Author.objects.all()[i + 1 :]:
                a1.followers.add(a2)

    def test_get_multiple_followers(self):
        alice = Author.objects.get(displayName="Alice")

        url = reverse(self.url_name, args=[alice.id])
        resp = self.client.get(url)

        self.assertEqual(resp.data["type"], "followers")
        self.assertEqual(len(resp.data["items"]), 2)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_one_follower(self):
        bob = Author.objects.get(displayName="Bob")
        carl = Author.objects.get(displayName="Carl")

        url = reverse(self.url_name, args=[bob.id])
        resp = self.client.get(url)

        self.assertEqual(resp.data["type"], "followers")
        self.assertEqual(len(resp.data["items"]), 1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        reconstruct = Author.objects.get(**resp.data["items"][0])
        self.assertEqual(reconstruct, carl)

    def test_get_no_followers(self):
        carl = Author.objects.get(displayName="Carl")

        url = reverse(self.url_name, args=[carl.id])
        resp = self.client.get(url)

        self.assertEqual(resp.data["type"], "followers")
        self.assertEqual(len(resp.data["items"]), 0)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_invalid_methods(self):
        carl = Author.objects.get(displayName="Carl")

        url = reverse(self.url_name, args=[carl.id])

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        resp = self.client.put(url)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_found(self):
        id = uuid.uuid4()
        url = reverse(self.url_name, args=[id])

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class FollowerAPITest(APITestCase):
    url_name = "project:api_follower"

    @classmethod
    def setUpTestData(cls):
        for name in ["Alice", "Bob"]:
            user = User.objects.create(username=name, password="testpassword1")
            Author.objects.create(user=user, displayName=name)

    def setUp(self):
        self.alice = Author.objects.get(displayName="Alice")
        self.bob = Author.objects.get(displayName="Bob")
        self.alice.followers.add(self.bob)

    def test_get_follower(self):
        kwargs = {"pk": self.alice.id, "follower_id": self.bob.id}

        url = reverse(self.url_name, kwargs=kwargs)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_not_follower(self):
        kwargs = {"pk": self.bob.id, "follower_id": self.alice.id}

        url = reverse(self.url_name, kwargs=kwargs)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_author_not_found(self):
        kwargs = {"pk": uuid.uuid4(), "follower_id": uuid.uuid4()}
        url = reverse(self.url_name, kwargs=kwargs)

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        resp = self.client.put(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_method(self):
        kwargs = {"pk": self.alice.id, "follower_id": self.bob.id}
        url = reverse(self.url_name, kwargs=kwargs)

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_follower(self):
        kwargs = {"pk": self.bob.id, "follower_id": self.alice.id}

        url = reverse(self.url_name, kwargs=kwargs)
        resp = self.client.put(url)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.bob.followers.first(), self.alice)

    def test_put_duplicate(self):
        kwargs = {"pk": self.alice.id, "follower_id": self.bob.id}

        url = reverse(self.url_name, kwargs=kwargs)
        resp = self.client.put(url)

        # What is our intended behaviour?
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_delete_follower(self):
        kwargs = {"pk": self.alice.id, "follower_id": self.bob.id}

        url = reverse(self.url_name, kwargs=kwargs)
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.alice.followers.exists())

    def test_delete_nonexistent(self):
        kwargs = {"pk": self.bob.id, "follower_id": self.alice.id}

        url = reverse(self.url_name, kwargs=kwargs)
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_maintain_reverse(self):
        self.alice.following.add(self.bob)
        kwargs = {"pk": self.alice.id, "follower_id": self.bob.id}

        url = reverse(self.url_name, kwargs=kwargs)
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.alice.following.first(), self.bob)
