from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Author


class CreatePostForm(forms.ModelForm):
    # TODO Constants should be referenced from a class attribute or constant variable, not a literal.
    # TODO Handle validation errors, eg when required field is empty

    title = forms.CharField(max_length=50, label="Title", required=True)

    description = forms.CharField(max_length=200, label="Description", required=True)

    content = forms.CharField(max_length=600, label="Content", required=True)

    # TODO Modify this and the Post model field to be a list of str.
    categories = forms.CharField(max_length=200, label="Categories")

    visibility = forms.ChoiceField(
        label="Visibility", choices=Post.VisibilityChoice.choices
    )

    unlisted = forms.BooleanField(label="Unlisted?", required=False)

    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "content",
            "categories",
            "visibility",
            "unlisted",
        ]


# TODO delete?
class EditPostForm(forms.ModelForm):
    # NOTE Code almost identical to CreatePostForm. Changes made there should probably be made here
    # TODO Constants should be referenced from a class attribute or constant variable, not a literal.
    # TODO Handle validation errors, eg when required field is empty

    title = forms.CharField(max_length=50, label="Title", required=True)

    description = forms.CharField(max_length=200, label="Description", required=True)

    content = forms.CharField(max_length=600, label="Content", required=True)

    # TODO Modify this and the Post model field to be a list of str.
    categories = forms.CharField(max_length=200, label="Categories")

    visibility = forms.ChoiceField(
        label="Visibility", choices=Post.VisibilityChoice.choices
    )

    unlisted = forms.BooleanField(label="Unlisted?", required=False)

    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "content",
            "categories",
            "visibility",
            "unlisted",
        ]


# References:
# https://stackoverflow.com/questions/22567320/django-edit-user-profile
# https://www.javatpoint.com/django-usercreationform
class AuthorCreationForm(UserCreationForm):
    username = forms.CharField(
        help_text="Enter a unique username"
    )  # required for the user, copy for displayName below
    github = forms.CharField(required=False, help_text="Optional")

    class Meta:
        model = User
        fields = ("username", "github", "password1", "password2")

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")

        # implement the uniqueness and correct password checking by hand
        # automatically checks for strong passwords
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise ValidationError("Passwords do not match!")

    def save(self, commit=True):
        user = super(AuthorCreationForm, self).save(commit=False)

        # https://stackoverflow.com/questions/48049247/how-to-set-is-active-false-in-django-usercreationform
        user.is_active = False  # Admin must activate new users

        if commit:
            user.save()
            author = Author.objects.create(
                user=user,
                displayName=self.cleaned_data.get("username"),
                github=self.cleaned_data.get("github"),
            )
            author.save()
        return user


# The author can only update their github link and bio
class EditProfileForm(forms.ModelForm):
    github = forms.CharField(required=False)
    bio = forms.CharField(required=False)

    class Meta:
        model = Author
        fields = ["github", "bio"]
