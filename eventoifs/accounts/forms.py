"""
Formulários do app accounts (SPEC seção 5.1).

FormCadastro  — cadastro de novo usuário (herda UserCreationForm)
FormPerfil    — edição do perfil complementar (herda ModelForm)
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Perfil


class FormCadastro(UserCreationForm):
    """
    Formulário de cadastro de usuário.
    Valida unicidade do e-mail no sistema.
    """
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classe Bootstrap a todos os campos gerados pela classe pai
        for field_name in ('password1', 'password2'):
            self.fields[field_name].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        """Garante que o e-mail informado ainda não está em uso."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado no sistema.')
        return email


class FormPerfil(forms.ModelForm):
    """
    Formulário de edição do perfil complementar.
    Valida que a matrícula contém apenas dígitos.
    """

    class Meta:
        model = Perfil
        fields = ('curso', 'matricula', 'bio')
        widgets = {
            'curso':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Informática'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Somente números'}),
            'bio':       forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_matricula(self):
        """Permite campo vazio; quando preenchido, exige somente dígitos."""
        matricula = self.cleaned_data.get('matricula', '')
        if matricula and not matricula.isdigit():
            raise forms.ValidationError('A matrícula deve conter apenas números.')
        return matricula
