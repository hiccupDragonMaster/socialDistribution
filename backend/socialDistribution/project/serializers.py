from rest_framework import serializers

# Add your serializers here.
from .models import Author, FollowRequest, Post, Node


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "url", "host", "displayName", "github", "profileImage"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "id",
            "source",
            "origin",
            "description",
            "contentType",
            "content",
            "author",
            "categories",
            "count",
            "published",
            "visibility",
            "unlisted",
        ]


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ["id", "nodeName", "apiURL", "host"]

    def create(self, validated_data):
        """
        Create and return a new `Node` instance, given the validated data
        """
        return Node.object.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Node` instance, given the validated data
        """
        instance.id = validated_data.get("id", instance.id)
        instance.nodeName = validated_data.get("nodeName", instance.nodeName)
        instance.apiURL = validated_data.get("apiURL", instance.apiURL)
        instance.host = validated_data.get("host", instance.host)


class FollowRequestSerializer(serializers.ModelSerializer):
    follower = AuthorSerializer()
    following = AuthorSerializer()

    class Meta:
        model = FollowRequest
        fields = ["summary", "follower", "following"]

    def create(self, validated_data):
        follower = Author.objects.get(**validated_data["follower"])
        following = Author.objects.get(**validated_data["following"])
        summary = validated_data["summary"]
        return FollowRequest.objects.create(
            follower=follower, following=following, summary=summary
        )

    def to_representation(self, instance):
        results = super().to_representation(instance)
        results["type"] = "Follow"
        results["actor"] = results.pop("follower", {})
        results["object"] = results.pop("following", {})
        return results

    def to_internal_value(self, data):
        data["follower"] = data.pop("actor", {})
        data["following"] = data.pop("object", {})
        return super().to_internal_value(data)
