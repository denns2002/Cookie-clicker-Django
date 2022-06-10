from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import \
    validate_password


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm')

    username = forms.CharField(
        max_length=20,
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
    )

    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password',
    )

    password_confirm = forms.CharField(
        max_length=20,
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}),
    )

    # change base methods
    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if validate_password(password) is None:
            if password == password_confirm:
                return cleaned_data
            raise forms.ValidationError('Passwords not equals!')
        else:
            raise forms.ValidationError('Password must meet complexity requirements')


    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user
