"""
Formulários do app eventos (SPEC seção 5.2).

FormEvento  — CRUD de eventos com validação personalizada (RF06)
FormBusca   — busca/filtro via GET (RF07)
"""

from django import forms
from .models import Evento, Categoria


class FormEvento(forms.ModelForm):
    """
    Formulário de criação/edição de evento.
    Validações obrigatórias:
      - data_fim posterior a data_inicio (RF06)
      - vagas maior que zero (RF06)
    """

    class Meta:
        model = Evento
        fields = (
            'titulo', 'descricao', 'local',
            'data_inicio', 'data_fim',
            'vagas', 'tipo', 'status', 'categorias',
        )
        widgets = {
            'titulo':      forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do evento',
            }),
            'descricao':   forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
            'local':       forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Auditório do bloco A',
            }),
            'data_inicio': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'data_fim':    forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'vagas':       forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'tipo':        forms.Select(attrs={'class': 'form-select'}),
            'status':      forms.Select(attrs={'class': 'form-select'}),
            'categorias':  forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formato compatível com input type=datetime-local
        self.fields['data_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['data_fim'].input_formats    = ['%Y-%m-%dT%H:%M']

    def clean(self):
        """Valida regras de negócio inter-campos."""
        cleaned = super().clean()
        data_inicio = cleaned.get('data_inicio')
        data_fim    = cleaned.get('data_fim')
        vagas       = cleaned.get('vagas')

        if data_inicio and data_fim and data_fim <= data_inicio:
            raise forms.ValidationError(
                'A data de fim deve ser posterior à data de início.'
            )

        if vagas is not None and vagas <= 0:
            self.add_error('vagas', 'O número de vagas deve ser maior que zero.')

        return cleaned


class FormBusca(forms.Form):
    """
    Formulário simples de busca/filtro (método GET).
    Campos: texto livre, categoria e status.
    """
    q = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título ou descrição...',
        }),
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        label='Categoria',
        empty_label='Todas as categorias',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    status = forms.ChoiceField(
        choices=[('', 'Todos os status')] + list(Evento.STATUS_CHOICES),
        required=False,
        label='Status',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
