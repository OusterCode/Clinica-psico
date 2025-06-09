from django import forms
from .models import Patients, Therapist, Agendamento
from .utils import is_valid_cpf, is_valid_phone, get_address_by_cep
from django.core.exceptions import ValidationError

class AbstractPersonForm(forms.ModelForm):
    class Meta:
        abstract = True
        fields = [
            'name', 'email', 'telephone', 'cpf', 'birth_date', 'photo',
            'CEP', 'address', 'numero', 'city', 'state'
        ]
        labels = {
            'name': 'Nome completo',
            'email': 'E-mail',
            'telephone': 'Telefone',
            'cpf': 'CPF',
            'birth_date': 'Data de nascimento',
            'photo': 'Foto',
            'CEP': 'CEP',
            'address': 'Endereço',
            'numero': 'Número',
            'city': 'Cidade',
            'state': 'Estado',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'email': forms.EmailInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'telephone': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'cpf': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'block w-full text-gray-900'}),
            'CEP': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400', 'id': 'CEP'}),
            'address': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400', 'id': 'address'}),
            'numero': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'city': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400', 'id': 'city'}),
            'state': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400', 'id': 'state'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not is_valid_cpf(cpf):
            raise ValidationError('CPF inválido.')
        return cpf

    def clean_telephone(self):
        telefone = self.cleaned_data.get('telephone')
        if telefone and not is_valid_phone(telefone):
            raise ValidationError('Telefone inválido. Use o formato (XX) 9XXXX-XXXX.')
        return telefone

class PatientForm(AbstractPersonForm):
    class Meta(AbstractPersonForm.Meta):
        model = Patients
        fields = AbstractPersonForm.Meta.fields + ['treatment']
        labels = dict(AbstractPersonForm.Meta.labels, **{
            'treatment': 'Queixa',
        })
        help_texts = {
            'cpf': 'Digite apenas números.',
            'telephone': 'Formato: (XX) 9XXXX-XXXX',
            'birth_date': 'Selecione no calendário ou digite no formato AAAA-MM-DD',
        }
        widgets = dict(AbstractPersonForm.Meta.widgets, **{
            'treatment': forms.Select(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
        })

    def clean_CEP(self):
        cep = self.cleaned_data.get('CEP')
        if cep:
            endereco = get_address_by_cep(cep)
            if not endereco:
                raise ValidationError('CEP inválido.')
            if not self.cleaned_data.get('address'):
                self.cleaned_data['address'] = endereco['address']
            if not self.cleaned_data.get('city'):
                self.cleaned_data['city'] = endereco['city']
            if not self.cleaned_data.get('state'):
                self.cleaned_data['state'] = endereco['state']
        return cep

class TherapistForm(AbstractPersonForm):
    class Meta(AbstractPersonForm.Meta):
        model = Therapist
        fields = AbstractPersonForm.Meta.fields + [
            'degree', 'treatments', 'is_subleasing', 'hourly_rate', 'available_days', 'available_times'
        ]
        labels = dict(AbstractPersonForm.Meta.labels, **{
            'degree': 'Grau de formação',
            'treatments': 'Queixas que pode tratar',
            'is_subleasing': 'Subloca consultório?',
            'hourly_rate': 'Valor da hora (R$)',
            'available_days': 'Dias disponíveis',
            'available_times': 'Horários disponíveis',
        })
        help_texts = {
            'cpf': 'Digite apenas números.',
            'telephone': 'Formato: (XX) 9XXXX-XXXX',
            'birth_date': 'Selecione no calendário ou digite no formato AAAA-MM-DD',
            'treatments': 'Segure Ctrl para selecionar mais de uma opção.',
        }
        widgets = dict(AbstractPersonForm.Meta.widgets, **{
            'degree': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'treatments': forms.SelectMultiple(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'is_subleasing': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400', 'step': '0.01'}),
            'available_days': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
            'available_times': forms.TextInput(attrs={'class': 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-gray-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none placeholder-gray-400'}),
        })

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['data', 'hora', 'terapeuta', 'paciente', 'observacoes', 'duracao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'duracao': forms.NumberInput(attrs={'type': 'number', 'class': 'form-input', 'min': 1, 'max': 240, 'step': 5}),
        }
