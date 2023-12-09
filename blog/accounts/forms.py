from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=12, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'profile_picture', 'phone_number')


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class CustomUserPasswordResetForm(PasswordResetForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class SetPasswordForm(PasswordResetForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    def clean_new_password2(self):
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']
        if new_password1 != new_password2:
            raise forms.ValidationError('Passwords don\'t match')
        return new_password2
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data