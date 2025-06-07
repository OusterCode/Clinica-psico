from django import forms
from .models import Patients, Therapist
from .utils import is_valid_cpf, is_valid_phone, get_address_by_cep
from django.core.exceptions import ValidationError

class AbstractPersonForm(forms.ModelForm):
    class Meta:
        abstract = True
        fields = ['name', 'email', 'telephone', 'cpf', 'birth_date', 'photo']
        labels = {
            'name': 'Nome completo',
            'email': 'E-mail',
            'telephone': 'Telefone',
            'cpf': 'CPF',
            'birth_date': 'Data de nascimento',
            'photo': 'Foto',
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
    class Meta:
        model = Patients
        fields = ['name', 'email', 'telephone', 'cpf', 'birth_date', 'photo', 'complaint', 'CEP', 'address', 'numero', 'city', 'state']
        labels = {
            'name': 'Nome completo',
            'email': 'E-mail',
            'telephone': 'Telefone',
            'cpf': 'CPF',
            'birth_date': 'Data de nascimento',
            'photo': 'Foto',
            'complaint': 'Queixa',
            'CEP': 'CEP',
            'address': 'Endereço',
            'numero': 'Número',
            'city': 'Cidade',
            'state': 'Estado',
        }
        help_texts = {
            'cpf': 'Digite apenas números.',
            'telephone': 'Formato: (XX) 9XXXX-XXXX',
            'birth_date': 'Selecione no calendário ou digite no formato AAAA-MM-DD',
        }

    def clean_CEP(self):
        cep = self.cleaned_data.get('CEP')
        if cep:
            endereco = get_address_by_cep(cep)
            if not endereco:
                raise ValidationError('CEP inválido.')
            # Preenche os campos de endereço se não informados
            if not self.cleaned_data.get('address'):
                self.cleaned_data['address'] = endereco['address']
            if not self.cleaned_data.get('city'):
                self.cleaned_data['city'] = endereco['city']
            if not self.cleaned_data.get('state'):
                self.cleaned_data['state'] = endereco['state']
        return cep

class TherapistForm(AbstractPersonForm):
    class Meta:
        model = Therapist
        fields = ['name', 'email', 'telephone', 'cpf', 'birth_date', 'photo', 'degree', 'complaints', 'is_subleasing', 'hourly_rate', 'available_days', 'available_times']
        labels = {
            'name': 'Nome completo',
            'email': 'E-mail',
            'telephone': 'Telefone',
            'cpf': 'CPF',
            'birth_date': 'Data de nascimento',
            'photo': 'Foto',
            'degree': 'Grau de formação',
            'complaints': 'Queixas que pode tratar',
            'is_subleasing': 'Subloca consultório?',
            'hourly_rate': 'Valor da hora (R$)',
            'available_days': 'Dias disponíveis',
            'available_times': 'Horários disponíveis',
        }
        help_texts = {
            'cpf': 'Digite apenas números.',
            'telephone': 'Formato: (XX) 9XXXX-XXXX',
            'birth_date': 'Selecione no calendário ou digite no formato AAAA-MM-DD',
            'complaints': 'Segure Ctrl para selecionar mais de uma opção.',
        }
