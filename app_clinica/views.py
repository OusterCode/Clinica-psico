from django.shortcuts import render, redirect
from .models import Patients, Tasks, Consultations, Treatment
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
from .utils import is_valid_cpf, is_valid_phone, get_address_by_cep
from django.core.files import File
import os
from .forms import PatientForm, TherapistForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

def index(request):
    return render(request, 'index.html')

@login_required
def pacientes(request):
    if request.method == "GET":
        patients = Patients.objects.all()
        treatments = Treatment.objects.all()
        # Valor default para o campo treatment: tratamento com code='Terapia'
        default_treatment = treatments.filter(code='Terapia').first()
        form_initial = {}
        if default_treatment:
            form_initial['treatment'] = default_treatment.id
        return render(request, 'cadastro_paciente.html', {
            'treatments': treatments,
            'patients': patients,
            'form': PatientForm(initial=form_initial),
        })
    else:
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso.')
            return redirect('patients')
        patients = Patients.objects.all()
        treatments = Treatment.objects.all()
        return render(request, 'cadastro_paciente.html', {
            'treatments': treatments,
            'patients': patients,
            'form': form,
            'erros': set(form.errors.keys()),
            'dados': request.POST,
        })
    
@login_required
def paciente_view(request, id):
    patient = Patients.objects.get(id=id)
    if request.method == "GET":
        tasks = Tasks.objects.all()
        consultations = Consultations.objects.filter(patient=patient)
        
        tuple_grafico = ([str(i.date) for i in consultations], [str(i.mood) for i in consultations])
        
        return render(request, 'paciente.html', {'patient': patient, 'tasks': tasks, 'consultations': consultations, 'tuple_grafico': tuple_grafico})
    else:
        mood = request.POST.get('mood')
        general_registration = request.POST.get('general_registration')
        video = request.FILES.get('video')
        tarefas = request.POST.getlist('tarefas')

        consultations = Consultations(
            mood=int(mood),
            general_registration=general_registration,
            video=video,
            patient=patient
        )
        consultations.save()

        for i in tarefas:
            task = Tasks.objects.get(id=i)
            consultations.tasks.add(task)

        consultations.save()

        messages.add_message(request, constants.SUCCESS, 'Registro de consulta adicionado com sucesso.')
        return redirect(f'/patients/{id}')
    
@login_required
def update_patient(request, id):
    patient = Patients.objects.get(id=id)
    payment_on_day = request.POST.get('payment_on_day')
    status = True if payment_on_day == 'active' else False
    patient.payment_on_day = status
    patient.save()
    return redirect(f'/patients/{id}')

@login_required
def delete_consultation(request, id):
    consultation = Consultations.objects.get(id=id)
    consultation.delete()
    return redirect(f'/patients/{consultation.patient.id}')

@login_required
def public_consultation(request, id):
    consultation = Consultations.objects.get(id=id)
    if not consultation.patient.payment_on_day:
        raise Http404()

    return render(request, 'public_consultation.html', {'consulta': consultation})

@login_required
def cadastrar_terapeuta(request):
    if request.method == "GET":
        treatments = Treatment.objects.all()
        # Valor default para o campo treatment: tratamento com code='Terapia'
        default_treatment = treatments.filter(code='Terapia').first()
        form_initial = {}
        if default_treatment:
            form_initial['treatment'] = default_treatment.id
        return render(request, 'cadastro_terapeuta.html', {'treatments': treatments, 'form': TherapistForm(initial=form_initial)})
    else:
        form = TherapistForm(request.POST, request.FILES)
        if form.is_valid():
            terapeuta = form.save()
            messages.add_message(request, constants.SUCCESS, 'Terapeuta cadastrado com sucesso!')
            return redirect('cadastrar_terapeuta')
        else:
            treatments = Treatment.objects.all()
            return render(request, 'cadastro_terapeuta.html', {
                'treatments': treatments,
                'form': form,
                'erros': set(form.errors.keys()),
                'dados': request.POST
            })

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

@login_required
def pacientes_cadastrados(request):
    patients = Patients.objects.all()
    return render(request, 'pacientes_cadastrados.html', {'patients': patients})