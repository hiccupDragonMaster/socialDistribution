from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

import uuid

from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Author, FollowRequest
from ..serializers import FollowRequestSerializer, AuthorSerializer


class FollowRequestSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        data = {
            "github": "http://www.github.com",
            "url": "http://www.google.com",
            "host": "::1",
        }

        for name in ["Alice", "Bob"]:
            user = User.objects.create(username=name, password="testpassword1")
            Author.objects.create(user=user, displayName=name, **data)

    def setUp(self):
        self.alice = Author.objects.get(displayName="Alice")
        self.bob = Author.objects.get(displayName="Bob")
        self.summary = "Bob wants to follow Alice"
        self.fr = FollowRequest.objects.create(
            follower=self.bob, following=self.alice, summary=self.summary
        )

    def test_follow_request_serialized(self):
        serializer = FollowRequestSerializer(self.fr)
        obj_type = serializer.data["type"]
        summary = serializer.data["summary"]
        follower = serializer.data["actor"]
        following = serializer.data["object"]

        self.assertEqual(obj_type, "Follow")
        self.assertEqual(summary, self.summary)
        self.assertEqual(Author.objects.get(**follower), self.bob)
        self.assertEqual(Author.objects.get(**following), self.alice)

    def test_follow_request_deserialized(self):
        data = {
            "type": "Follow",
            "summary": self.summary,
            "actor": AuthorSerializer(self.bob).data,
            "object": AuthorSerializer(self.alice).data,
        }

        serializer = FollowRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        follower = Author.objects.get(**serializer.validated_data["follower"])
        following = Author.objects.get(**serializer.validated_data["following"])
        summary = serializer.validated_data["summary"]
        fr = FollowRequest.objects.get(
            follower=follower, following=following, summary=summary
        )
        self.assertEqual(fr, self.fr)

    def test_invalid_request(self):
        data = {"blah": "blah"}
        # Should probably check type field as well!
        serializer = FollowRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class FollowRequestAPITest(APITestCase):
    url_name = "project:api_follow_request"

    @classmethod
    def setUpTestData(cls):
        data = {
            "github": "http://www.github.com",
            "url": "http://www.google.com",
            "host": "::1",
        }

        for name in ["Alice", "Bob"]:
            user = User.objects.create(username=name, password="testpassword1")
            Author.objects.create(user=user, displayName=name, **data)

    def setUp(self):
        self.alice = Author.objects.get(displayName="Alice")
        self.bob = Author.objects.get(displayName="Bob")
        self.summary = "Bob wants to follow Alice"
        fr = FollowRequest.objects.create(
            follower=self.bob, following=self.alice, summary=self.summary
        )
        self.serializer = FollowRequestSerializer(fr)
        fr.delete()

    def test_posted_successfully(self):
        url = reverse(self.url_name, args=[self.alice.id])

        resp = self.client.post(url, self.serializer.data, format="json")

        query = FollowRequest.objects.filter(
            follower=self.bob, following=self.alice, summary=self.summary
        )
        self.assertTrue(query.exists())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_author_not_found(self):
        fake_id = uuid.uuid4()
        url = reverse(self.url_name, args=[fake_id])

        resp = self.client.post(url, self.serializer.data, format="json")
        query = FollowRequest.objects.filter(
            follower=self.bob, following=self.alice, summary=self.summary
        )
        self.assertFalse(query.exists())
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_data(self):
        # Need to test more of these cases depending on how we want it to work
        url = reverse(self.url_name, args=[self.alice.id])
        data = self.serializer.data
        data.pop("summary")

        resp = self.client.post(url, data, format="json")
        query = FollowRequest.objects.filter(follower=self.bob, following=self.alice)
        self.assertFalse(query.exists())
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
