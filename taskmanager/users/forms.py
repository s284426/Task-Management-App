from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_superuser = forms.BooleanField(
        required=False,
        label='Create as Administrator',
        help_text='Check this box to create an administrator account'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['is_superuser']:
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user
    

# Note: You have a duplicate UserRegisterForm class - you should remove one of them
# I'm keeping the second one here but you should decide which one to use

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']