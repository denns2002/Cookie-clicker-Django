from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm')

    username = forms.CharField(
        max_length=20,
        label='Your Username',
        widget=forms.TextInput(attrs={'placeholder': 'Enter'}),
    )

    password = forms.CharField(
        min_length=3,
        max_length=20,
        label='Your Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
    )

    password_confirm = forms.CharField(
        min_length=3,
        max_length=20,
        label='Password Confirmation',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}),
    )

    # change base methods
    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password == password_confirm:
            return cleaned_data
        raise forms.ValidationError('Passwords not equals each other~!<3')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user
