
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nome = forms.CharField(max_length=100, required=True)
    endereco = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nome', 'endereco']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            perfil = Perfil(user=user,username= self.cleaned_data['username'],  nome=self.cleaned_data['nome'], endereco=self.cleaned_data['endereco'], email=self.cleaned_data['email'])
            perfil.save()
        return user
