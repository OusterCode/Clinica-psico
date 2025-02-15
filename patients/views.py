from django.shortcuts import render, redirect
from .models import Patients, Tasks, Consultations
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404

def patients(request):
    
    if request.method == "GET":
        patients= Patients.objects.all()
        return render(request, 'patients.html', {'complaints': Patients.complaint_choices, 'patients': patients})
    
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        complaint = request.POST.get('complaint')
        photo = request.FILES.get('photo')

        if len(name.strip()) == 0 or not photo:
            messages.add_message(request, constants.ERROR, 'The name and photo fields are mandatory')
            return redirect('patients')

        patient = Patients(
            name=name,
            email=email,
            telephone=telephone,
            complaint=complaint,
            photo=photo
        )
        # Saves in the database
        patient.save()

        messages.add_message(request, constants.SUCCESS, 'Patient added successfully')
        return redirect('patients')
    
def patient_view(request, id):
    patient = Patients.objects.get(id=id)
    if request.method == "GET":
        tasks = Tasks.objects.all()
        consultations = Consultations.objects.filter(patient=patient)
        
        tuple_grafico = ([str(i.date) for i in consultations], [str(i.mood) for i in consultations])
        
        return render(request, 'patient.html', {'patient': patient, 'tasks': tasks, 'consultations': consultations, 'tuple_grafico': tuple_grafico})
    else:
        mood = request.POST.get('mood')
        general_registration = request.POST.get('general_registration')
        video = request.FILES.get('video')
        tasks = request.POST.getlist('tasks')

        consultations = Consultations(
            mood=int(mood),
            general_registration=general_registration,
            video=video,
            patient=patient
        )
        consultations.save()

        for i in tasks:
            task = Tasks.objects.get(id=i)
            consultations.tasks.add(task)

        consultations.save()

        messages.add_message(request, constants.SUCCESS, 'Query record added successfully.')
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

    return render(request, 'public_consultation.html', {'consultation': consultation})