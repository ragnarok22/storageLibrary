from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from accounts.models import Profile


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )


class CreateProfileForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirme contraseña',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")  # Passwords don't match
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        # save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']
