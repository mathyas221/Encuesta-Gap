from django.forms import ModelForm
from Questions.models import Personal
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PersonalForm(ModelForm):
    class Meta:
        model = Personal
        fields = ['position']
        labels = {
            'position': 'Cargo'
        }
        widgets = {
            'position': forms.Select(attrs={'class': 'form-control'})
        }


class UserForm(ModelForm):
    password1 = forms.CharField(label='Ingrese contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre de usuario'}),
        }
