from django.urls import path
from . import views

app_name = "project"
urlpatterns = [
    path("create-post", views.CreatePostView.as_view(), name="create-post"),
    path("edit-post/<str:pk>", views.EditPostView.as_view(), name="edit-post"),
    # Stream
    path("<str:username>/stream", views.StreamView.as_view(), name="stream"),
    # Author
    path("<str:pk>", views.AuthorView.as_view(), name="author"),
    # Post
    path("posts/<str:pk>", views.PostView.as_view(), name="post"),
    # Profile
    path("<str:pk>/profile", views.ProfileView.as_view(), name="profile"),
    # Edit Profile
    path("edit/", views.profile_edit, name="profile_edit"),
    # Homepage
    path("", views.stream_view, name="home"),
    # Signup
    path("signup/", views.SignupView.as_view(), name="signup"),
    # API
    path("api/authors/", views.AuthorAPIView.as_view(), name="get_authors"),
    path("api/authors/<str:pk>/", views.update_author, name="author_api"),
    path("api/authors/<str:pk>/posts/", views.new_post_api, name="new_post_api"),
    path(
        "api/authors/<str:pk>/posts/<str:post_id>",
        views.update_post_api,
        name="update_post_api",
    ),
    path("api/authors/<str:pk>/inbox", views.update_inbox, name="inbox_api"),
    path("api/nodes/", views.NodeAPIView.as_view(), name="node_api"),
    # Likes
    path("post/<str:pk>/like/", views.like_post, name="like_post"),
    # Comments
    path("post/<str:pk>/comment/", views.add_comment, name="add_comment"),
    # Follow
    path("author/<str:pk>/follow/", views.send_follow_request, name="follow"),
    # Accept follow request
    path(
        "followrequest/<str:pk>/accept/",
        views.accept_follow_request,
        name="accept_follow",
    ),
    # Decline follow request
    path(
        "followrequest/<str:pk>/decline/",
        views.decline_follow_request,
        name="decline_follow",
    ),
    # Decline follow request
    path("author/<str:pk>/unfollow/", views.unfollow, name="unfollow"),
    path("search/", views.SearchAuthors.as_view(), name="search"),
    # Follow API
    path(
        "api/authors/<str:pk>/followers/",
        views.FollowersAPIView.as_view(),
        name="get_followers",
    ),
    path(
        "api/authors/<str:pk>/followers/<str:follower_id>",
        views.FollowerAPIView.as_view(),
        name="api_follower",
    ),
    path(
        "api/authors/<str:pk>/inbox/followrequest",
        views.FollowRequestAPIView.as_view(),
        name="api_follow_request",
    ),
    path("post/<str:pk>/delete", views.delete_post, name="post_delete"),
]
