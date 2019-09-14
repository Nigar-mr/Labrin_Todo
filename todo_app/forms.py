from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import authenticate
from todo_app.models import MyUser, Post, CommentModel

User = MyUser


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_(
                                             "Raw şifrələr bazada saxlanmır, onları heç cürə görmək mümkün deyil "
                                             "bu istifadəçinin şifrəsidir, lakin siz onu dəyişə bilərsiziniz "
                                             " <a href=\"../password/\">bu form</a>. vasitəsilə"))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "input100",
            "type": "text",
            "name": "username",
            "placeholder": "Username"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "input100",
            "type": "password",
            "name": "password",
            "placeholder": "Password"
        }
    ))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "input100",
            'type': "text",
            'name': "pass",
            "placeholder": "*************"
        }
    ))
    confirm_password = forms.CharField(label="Repeat password", widget=forms.PasswordInput(
        attrs={
            "class": "input100",
            'type': "text",
            'name': "repeat-pass",
            "placeholder": "*************"
        }
    ))

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Password not match!!!")

    class Meta:
        model = MyUser

        fields = [
            'full_name', 'email', 'username', 'profile_image'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': "input100",
                'type': "text",
                'name': "name",
                'placeholder': "Name..."
            }),
            'email': forms.EmailInput(attrs={
                'class': "input100",
                'type': "text",
                'name': "email",
                'placeholder': "Email addess..."
            }),
            'username': forms.TextInput(attrs={
                'class': "input100",
                'type': "text",
                'name': "username",
                'placeholder': "Username..."
            })
        }


class PostForm(forms.ModelForm):

    more = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': "form-control input-lg",
        'type': 'text',
        'placeholder': 'More'
    }))
    datetime = forms.DateTimeField(input_formats=["%m/%d/%Y %H:%M %p"])

    class Meta:
        model = Post
        fields = [
            'name', 'more', 'datetime'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control input-lg",
                'type': 'text',
                'placeholder': 'Name'
            })
        }

class ShareForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "input100",
            "type": "text",
            "name": "username",
            "placeholder": "Username"
        }
    ))

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment']

        widgets = {
            'comment': forms.TextInput(attrs={
                # 'type': "text",
                'class': "form-control",
                'placeholder': "Leave a comment...",
                'id': "comment",
                'name': 'room-name-input',
            })
        }
