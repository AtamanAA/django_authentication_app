from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Name",
        max_length=15,
        error_messages={"max_length": "Use a shorter name"},
    )
    email = forms.EmailField(
        label="E-mail",
        max_length=40,
        error_messages={"invalid": "Enter the correct email address!"},
    )
    password1 = forms.CharField(
        label="Password", max_length=20, widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Repeat password", max_length=20, widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields do not match!")
        return password2


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Name",
        max_length=15,
        error_messages={"max_length": "Use a shorter name"},
    )
    password = forms.CharField(
        label="Password", max_length=20, widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"


class UpdateUserFormTEST(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        label="Name",
        max_length=15,
        error_messages={"max_length": "Use a shorter name"},
    )
    email = forms.EmailField(
        label="E-mail",
        max_length=40,
        error_messages={"invalid": "Enter the correct email address!"},
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control-plaintext"


class PasswordChangeUserForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password", max_length=20, widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label="New password", max_length=20, widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label="Confirmation new password", max_length=20, widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")

    def __init__(self, *args, **kwargs):
        super(PasswordChangeUserForm, self).__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs["class"] = "form-control"
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control"
