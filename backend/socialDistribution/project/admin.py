from django.contrib import admin
from .models import Author, FollowRequest, Post, Comment, PostLike, CommentLike, Node

# Register your models here.
admin.site.register(Author)
admin.site.register(FollowRequest)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Node)
