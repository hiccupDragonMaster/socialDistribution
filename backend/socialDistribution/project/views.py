from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AuthorCreationForm, EditProfileForm, CreatePostForm, EditPostForm
from .models import Author, Post, Comment, PostLike, FollowRequest, Node
from .serializers import (
    PostSerializer,
    AuthorSerializer,
    NodeSerializer,
    FollowRequestSerializer,
)


class AuthorView(generic.DetailView):
    template_name = "project/author.html"
    model = Author


class PostView(generic.DetailView):
    template_name = "project/post.html"
    model = Post


class StreamView(generic.ListView):
    template_name = "project/stream.html"
    context_object_name = "latest_posts"

    def get_queryset(self):
        self.author = get_object_or_404(Author, displayName=self.kwargs["username"])
        return self.author.streamPosts.order_by("-published")


def stream_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy("login"))

    author = request.user.author
    latest_posts = author.streamPosts.order_by("-published")

    # Fetch friend requests
    friend_requests = FollowRequest.objects.filter(following=author)

    context = {
        "latest_posts": latest_posts,
        "friend_requests": friend_requests,
    }
    return render(request, "project/stream.html", context)


class ProfileView(generic.DetailView):
    template_name = "project/profile.html"
    model = Author


@login_required
def profile_edit(request):
    # Edit the current user's profile
    logged_in_author = request.user.author

    if request.method == "GET":
        form = EditProfileForm(instance=logged_in_author)
        return render(request, "project/edit_profile.html", {"form": form})
    elif request.method == "POST":
        form = EditProfileForm(request.POST, instance=logged_in_author)

        # Given the navigation bar, no redirection is needed.
        if form.is_valid():
            if form.has_changed():
                form.save()

                # Only display notification if some changes were made
                messages.success(request, "Changes saved successfully")
            return HttpResponseRedirect(reverse("project:profile_edit"))
        else:
            # if the form input was not valid, try again
            messages.success(
                request, "Warning: not a valid Github link, changes discarded"
            )
            return HttpResponseRedirect(reverse("project:profile_edit"))


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "project/create-post.html"
    form_class = CreatePostForm
    login_url = "login"

    def form_valid(self, form):
        author = get_object_or_404(Author, pk=self.request.user.author.id)
        form.instance.author = author

        # TODO These are just placeholders. Need to figure out what to put here for part 2
        form.instance.source = "http://127.0.0.1:8000/"
        form.instance.origin = "http://127.0.0.1:8000/"

        form.instance.contentType = (
            "text/plain"  # TODO Change when implementing Markdown
        )
        form.instance.count = 0
        form.instance.published = datetime.now()

        return super(CreatePostView, self).form_valid(form)


# https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView
class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "project/edit-post.html"
    form_class = EditPostForm
    login_url = "login"

    # TODO check that the author is the current user


class SignupView(generic.CreateView):
    # Use custom form to connect author model to user creation
    form_class = AuthorCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    # Send a success notification to the redirected page (login page)
    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Account created. An admin will activate your account shortly.",
        )
        return HttpResponseRedirect(reverse("login"))


class AuthorAPIView(APIView):
    """
    Get the list of authors on our website
    """

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        full_response = {"type": "authors", "items": serializer.data}
        return Response(full_response)


@api_view(["GET", "POST"])
def update_author(request, pk):
    """
    Update or get a specific author
    """
    author = get_object_or_404(Author, id=pk)

    if request.method == "GET":
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(status=400, data=serializer.errors)
    if request.method == "POST":
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=400, data=serializer.errors)


@api_view(["GET", "POST"])
def new_post_api(request, pk):
    posts = Post.objects.filter(author=pk)

    if request.method == "GET":
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PostSerializer(posts, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=400, data=serializer.errors)


@api_view(["GET", "POST", "DELETE", "PUT"])
def update_post_api(request, pk, post_id):
    if request.method == "PUT":
        serializer = PostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=400, data=serializer.errors)

    post = get_object_or_404(Post, id=post_id)

    if request.method == "GET":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data, status=201)
        return Response(status=400, data=serializer.errors)
    if request.method == "POST":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=400, data=serializer.errors)
    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST", "DELETE"])
def update_inbox(request, pk):
    """
    Update an inbox
    """
    author = get_object_or_404(Author, id=pk)
    inbox = author.streamPosts.all()

    if request.method == "GET":
        serializer = PostSerializer(inbox, many=True)
        author_str = "http://" + str(author.host) + "/authors/" + str(author.id)
        full_response = {
            "type": "inbox",
            "author": author_str,
            "items": serializer.data,
        }
        return Response(full_response, status=201)

    if request.method == "POST":
        # TODO: if the type is not "post", then check for comments/likes/follows
        serializer = PostSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=400, data=serializer.errors)
    elif request.method == "DELETE":
        author.streamPosts.remove()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NodeAPIView(APIView):
    """
    Get the list of nodes
    """

    def get(self, request, *args, **kwargs):
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return Response(serializer.data)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        content = request.POST.get("content")
        Comment.objects.create(
            author=request.user.author,
            post=post,
            comment=content,
            contentType="text/plain",
        )  # Assuming contentType is plain text for this example
    return HttpResponseRedirect(reverse("project:post", args=[pk]))


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Check if the user already liked the post
    liked = PostLike.objects.filter(author=request.user.author, post=post).exists()
    if not liked:
        PostLike.objects.create(
            author=request.user.author,
            post=post,
            summary=f"{request.user.username} likes this",
            context=post.source,
        )
    else:
        PostLike.objects.filter(author=request.user.author, post=post).delete()
    return HttpResponseRedirect(reverse("project:post", args=[pk]))


# TODO none of these login decerators check who is logged in. anybody can accept requests on other people's behalfs right now.


@login_required
def send_follow_request(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        request_exists = FollowRequest.objects.filter(
            follower=request.user.author, following=author
        ).exists()
        if request.user.author.id != author.id and not request_exists:
            summary = f"{request.user.author.displayName} wants to follow {author.displayName}"
            FollowRequest.objects.create(
                follower=request.user.author, following=author, summary=summary
            )
    return redirect(reverse("project:profile", args=[pk]))


@login_required
def unfollow(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        request.user.author.following.remove(author)
    return redirect(reverse("project:profile", args=[pk]))


@login_required
def decline_follow_request(request, pk):
    fr = get_object_or_404(FollowRequest, pk=pk)
    if request.method == "POST":
        fr.delete()
    return redirect(reverse("project:home"))


@login_required
def accept_follow_request(request, pk):
    fr = get_object_or_404(FollowRequest, pk=pk)
    if request.method == "POST":
        fr.follower.following.add(fr.following)
        fr.delete()
    return redirect(reverse("project:home"))


class SearchAuthors(generic.ListView):
    template_name = "project/search-page.html"
    model = Author
    context_object_name = "userlist"

    def get_queryset(self):
        query = self.request.GET.get("username")
        if query is None:
            userlist = Author.objects.all().order_by("displayName")
            return userlist
        else:
            userlist = Author.objects.filter(displayName__icontains=query).order_by(
                "displayName"
            )
            return userlist


class FollowersAPIView(APIView):
    def get_queryset(self):
        author = get_object_or_404(Author, pk=self.kwargs["pk"])
        return author.followers.all()

    def get(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = AuthorSerializer(query_set, many=True)
        results = {"type": "followers", "items": serializer.data}
        return Response(results)


class FollowerAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Not sure what this should return in the response
        author = get_object_or_404(Author, pk=kwargs["pk"])
        follower = get_object_or_404(author.followers, pk=kwargs["follower_id"])
        serializer = AuthorSerializer(follower)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        author = get_object_or_404(Author, pk=kwargs["pk"])
        # Add to DB if necessary?
        follower = get_object_or_404(Author, pk=kwargs["follower_id"])
        author.followers.add(follower)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(Author, pk=kwargs["pk"])
        follower = get_object_or_404(author.followers, pk=kwargs["follower_id"])
        author.followers.remove(follower)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowRequestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        author = get_object_or_404(Author, pk=kwargs["pk"])
        serializer = FollowRequestSerializer(
            FollowRequest.objects.filter(following=author), many=True
        )
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Make sure author exists?
        get_object_or_404(Author, pk=kwargs["pk"])
        # Assumes other author is in the database?
        serializer = FollowRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=400, data=serializer.errors)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST" and post.author.id == request.user.author.id:
        print("DELETED!")
        post.delete()
    return redirect(reverse("project:home"))
