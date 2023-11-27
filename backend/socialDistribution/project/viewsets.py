from rest_framework import viewsets
from rest_framework.decorators import action

from . import serializers
from . import models


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.all()

    # TODO: add search filter

    @action(detail=True, methods=["POST"])
    def follow_request(self):
        ... # write follow request logic

    @action(detail=True, methods=["POST"])
    def unfollow(self):
        ...  # write unfollow request logic


class FollowRequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.FollowRequest.objects.all()

    def get_queryset(self):
        ... # Filter by request user

    @action(detail=True, methods=["POST"])
    def decline(self):
        ...  # write follow request logic

    @action(detail=True, methods=["POST"])
    def accept(self):
        ...  # write follow request logic


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()

    @action(detail=True, methods=["POST"])
    def like(self):
        ... # write like logic


    @action(detail=True, methods=["POST"])
    def comment(self):
        ... # write like logic


class FollowerViewSet(viewsets.ModelViewSet):
    ... # TODO: implement through model

class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NodeSerializer
    queryset = models.Node.objects.all()


class InboxViewSet(viewsets.ModelViewSet):
    ...  # create through model and manage explicitly

