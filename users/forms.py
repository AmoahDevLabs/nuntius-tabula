from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import User, Profile


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='email')


class UserChangingForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'first_name', 'last_name', 'password']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'first_name', 'last_name']


class PasswordUpdateForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'image': forms.FileInput(),
            'sex': forms.Select(),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'nickname': forms.TextInput(attrs={'placeholder': 'Add display name'}),
            'address': forms.TextInput(attrs={'placeholder': 'Add address'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add biography'})
        }


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

