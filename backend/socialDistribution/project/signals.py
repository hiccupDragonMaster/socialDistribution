from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


# stream update after post creation
@receiver(post_save, sender=Post)
def on_post_create(sender, instance, created, **kwargs):
    if created:
        post = instance
        author = instance.author

        followers = author.followers.all()

        # TODO there's probably a more efficient way to do this.
        for follower in followers:
            follower.streamPosts.add(post)

        print("post sent to stream inboxes:", post.title)
