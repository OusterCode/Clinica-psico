from django.shortcuts import render, redirect
from .models import Patients, Treatment, Therapist
from django.contrib import messages
from django.contrib.messages import constants
from .forms import PatientForm, TherapistForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db import models
from django.core.paginator import Paginator

# =========================
# Autenticação e Boas-vindas
# =========================

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('welcome')
        else:
            return render(request, 'login.html', {'form': {'errors': True}})
    return render(request, 'login.html', {'form': {}})

@login_required
def welcome(request):
    return render(request, 'welcome.html')

def logout_view(request):
    auth_logout(request)
    return redirect('index')

# =========================
# Pacientes
# =========================

@login_required
def cadastrar_paciente(request):
    if request.method == "GET":
        patients = Patients.objects.all()
        treatments = Treatment.objects.all()
        default_treatment = treatments.filter(code='Terapia').first()
        form_initial = {}
        if default_treatment:
            form_initial['treatment'] = default_treatment.id
        return render(request, 'pacientes/cadastro_paciente.html', {
            'treatments': treatments,
            'patients': patients,
            'form': PatientForm(initial=form_initial),
        })
    else:
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso.')
            return redirect('visualizar_pacientes')
        patients = Patients.objects.all()
        treatments = Treatment.objects.all()
        return render(request, 'pacientes/cadastro_paciente.html', {
            'treatments': treatments,
            'patients': patients,
            'form': form,
            'erros': set(form.errors.keys()),
            'dados': request.POST,
        })

@login_required
def pacientes_cadastrados(request):
    patients = Patients.objects.all()
    return render(request, 'pacientes_cadastrados.html', {'patients': patients})

@login_required
def visualizar_pacientes(request):
    query = request.GET.get('q', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page')
    if query:
        patients = Patients.objects.filter(
            models.Q(name__icontains=query) | models.Q(cpf__icontains=query)
        )
    else:
        patients = Patients.objects.all()
    paginator = Paginator(patients, per_page)
    page_obj = paginator.get_page(page_number)
    return render(request, 'pacientes/visualizar_pacientes.html', {
        'patients': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'query': query,
    })

@login_required
def editar_paciente(request, id):
    paciente = Patients.objects.get(id=id)
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Dados do paciente atualizados com sucesso.')
            return redirect('visualizar_pacientes')
    else:
        form = PatientForm(instance=paciente)
    return render(request, 'pacientes/editar_paciente.html', {'form': form, 'paciente': paciente})

@login_required
def excluir_paciente(request, id):
    paciente = Patients.objects.get(id=id)
    if request.method == "POST":
        paciente.delete()
        messages.add_message(request, constants.SUCCESS, 'Paciente excluído com sucesso.')
        return redirect('visualizar_pacientes')
    return render(request, 'pacientes/excluir_paciente.html', {'paciente': paciente})

# =========================
# Terapeutas
# =========================

@login_required
def cadastrar_terapeuta(request):
    if request.method == "GET":
        treatments = Treatment.objects.all()
        # Valor default para o campo treatment: tratamento com code='Terapia'
        default_treatment = treatments.filter(code='Terapia').first()
        form_initial = {}
        if default_treatment:
            form_initial['treatment'] = default_treatment.id
        return render(request, 'terapeuta/cadastro_terapeuta.html', {'treatments': treatments, 'form': TherapistForm(initial=form_initial)})
    else:
        form = TherapistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Terapeuta cadastrado com sucesso!')
            return redirect('visualizar_terapeutas')
        else:
            treatments = Treatment.objects.all()
            return render(request, 'terapeuta/cadastro_terapeuta.html', {
                'treatments': treatments,
                'form': form,
                'erros': set(form.errors.keys()),
                'dados': request.POST
            })

@login_required
def visualizar_terapeutas(request):
    query = request.GET.get('q', '').strip()
    per_page = int(request.GET.get('per_page', 10))
    page_number = request.GET.get('page')
    if query:
        terapeutas = Therapist.objects.filter(
            models.Q(name__icontains=query) | models.Q(cpf__icontains=query)
        )
    else:
        terapeutas = Therapist.objects.all()
    paginator = Paginator(terapeutas, per_page)
    page_obj = paginator.get_page(page_number)
    return render(request, 'terapeuta/visualizar_terapeutas.html', {
        'terapeutas': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'per_page': per_page,
        'query': query,
    })

@login_required
def editar_terapeuta(request, id):
    terapeuta = Therapist.objects.get(id=id)
    if request.method == "POST":
        form = TherapistForm(request.POST, request.FILES, instance=terapeuta)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Dados do terapeuta atualizados com sucesso.')
            return redirect('visualizar_terapeutas')
    else:
        form = TherapistForm(instance=terapeuta)
    return render(request, 'terapeuta/editar_terapeuta.html', {'form': form, 'terapeuta': terapeuta})

@login_required
def excluir_terapeuta(request, id):
    terapeuta = Therapist.objects.get(id=id)
    if request.method == "POST":
        terapeuta.delete()
        messages.add_message(request, constants.SUCCESS, 'Terapeuta excluído com sucesso.')
        return redirect('visualizar_terapeutas')
    return render(request, 'terapeuta/excluir_terapeuta.html', {'terapeuta': terapeuta})