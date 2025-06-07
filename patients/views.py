from django.shortcuts import render, redirect
from .models import Patients, Tasks, Consultations
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
from .utils import is_valid_cpf, is_valid_phone, get_address_by_cep
from django.core.files import File
import os
from .forms import PatientForm, TherapistForm

def index(request):
    return render(request, 'index.html')
    
def pacientes(request):
    if request.method == "GET":
        patients = Patients.objects.all()
        return render(request, 'cadastro_paciente.html', {'complaints': Patients.complaint_choices, 'patients': patients, 'form': PatientForm()})
    else:
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso.')
            return redirect('patients')
        else:
            patients = Patients.objects.all()
            return render(request, 'cadastro_paciente.html', {
                'complaints': Patients.complaint_choices,
                'patients': patients,
                'form': form,
                'erros': set(form.errors.keys()),
                'dados': request.POST
            })
    
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
    
def update_patient(request, id):
    patient = Patients.objects.get(id=id)
    payment_on_day = request.POST.get('payment_on_day')
    status = True if payment_on_day == 'active' else False
    patient.payment_on_day = status
    patient.save()
    return redirect(f'/patients/{id}')

def delete_consultation(request, id):
    consultation = Consultations.objects.get(id=id)
    consultation.delete()
    return redirect(f'/patients/{consultation.patient.id}')

def public_consultation(request, id):
    consultation = Consultations.objects.get(id=id)
    if not consultation.patient.payment_on_day:
        raise Http404()

    return render(request, 'public_consultation.html', {'consulta': consultation})

def cadastrar_terapeuta(request):
    from .models import Therapist, Complaint
    if request.method == "GET":
        complaints = Complaint.objects.all()
        return render(request, 'cadastro_terapeuta.html', {'complaints': complaints, 'form': TherapistForm()})
    else:
        form = TherapistForm(request.POST, request.FILES)
        if form.is_valid():
            terapeuta = form.save()
            # ManyToMany complaints já salvo pelo ModelForm
            messages.add_message(request, constants.SUCCESS, 'Terapeuta cadastrado com sucesso!')
            return redirect('cadastrar_terapeuta')
        else:
            complaints = Complaint.objects.all()
            return render(request, 'cadastro_terapeuta.html', {
                'complaints': complaints,
                'form': form,
                'erros': set(form.errors.keys()),
                'dados': request.POST
            })