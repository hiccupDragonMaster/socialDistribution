from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    url = models.URLField(max_length=200, blank=True, null=True)
    host = models.GenericIPAddressField(
        default="127.0.0.1"
    )  # TODO add conditional for localhost if not deployed
    displayName = models.CharField(max_length=50)
    github = models.URLField(max_length=200, blank=True)
    profileImage = models.URLField(
        max_length=200, default="https://i.imgur.com/k7XVwpB.jpeg"
    )

    bio = models.CharField(max_length=1000, blank=True)

    streamPosts = models.ManyToManyField("Post", related_name="inboxes", blank=True)
    following = models.ManyToManyField(
        "Author", related_name="followers", symmetrical=False, blank=True
    )


class FollowRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    summary = models.CharField(max_length=200)
    follower = models.ForeignKey(
        Author, related_name="outgoing_follow_requests", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        Author, related_name="incoming_follow_requests", on_delete=models.CASCADE
    )


class Post(models.Model):
    class VisibilityChoice(models.TextChoices):
        PUBLIC = "PUBLIC", "PUBLIC"
        PRIVATE = "PRIVATE", "PRIVATE"
        FRIENDS_ONLY = "FRIENDS_ONLY", "FRIENDS_ONLY"

    title = models.CharField(max_length=50, default="Untitled")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.URLField(max_length=200)
    origin = models.URLField(max_length=200)
    description = models.CharField(max_length=50, default="")
    contentType = models.CharField(max_length=200)
    content = models.TextField(max_length=600)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.CharField(max_length=200, default="")  # TODO Change to list
    count = models.IntegerField(default=0)
    published = models.DateTimeField(default=datetime.now, blank=True)
    visibility = models.CharField(
        max_length=50, choices=VisibilityChoice.choices, default=VisibilityChoice.PUBLIC
    )
    unlisted = models.BooleanField()

    def get_absolute_url(self):
        return reverse("project:post", kwargs={"pk": self.pk})


class Comment(models.Model):
    # TODO needs a foreign key for Post
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField(max_length=600)
    contentType = models.CharField(max_length=200)
    published = models.DateTimeField(default=datetime.now, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class PostLike(models.Model):
    context = models.URLField(max_length=200)
    summary = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class CommentLike(models.Model):
    context = models.URLField(max_length=200)
    summary = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nodeName = models.CharField(max_length=50)
    apiURL = models.URLField(max_length=200)
    host = models.GenericIPAddressField(default="127.0.0.1:8000")
