from django import forms
from .models import Registro
from django.contrib.auth.models import User


class RegistroForm(forms.ModelForm):

    class Meta:
        model = Registro
        fields = [
            'valor',
            'sin_boleta'
        ]


class UsuarioForm(forms.Form):

    username = forms.CharField(max_length=150)

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class CambiarPasswordForm(forms.Form):

    password_actual = forms.CharField(
        widget=forms.PasswordInput()
    )

    password_nueva = forms.CharField(
        widget=forms.PasswordInput()
    )

    confirmar_password = forms.CharField(
        widget=forms.PasswordInput()
    )