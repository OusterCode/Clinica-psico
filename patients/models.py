from django.db import models
from django.urls import reverse

class Patients(models.Model):
    complaint_choices = (
        ('ADHD', 'ADHD'),
        ('D', 'Depression'),
        ('A', 'Anxiety'),
        ('GAD', 'Generalized anxiety disorder')
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    complaint = models.CharField(max_length=4, choices=complaint_choices, default='ADHD')
    photo = models.ImageField(upload_to='photos')
    payment_on_day = models.BooleanField(default=True)

    # Magic method
    def __str__(self):
        return self.name
    
class Tasks(models.Model):
    frequence_choices = (
        ('D', 'Diary'),
        ('1S', '1 time per week'),
        ('2S', '2 time per week'),
        ('3S', '3 time per week'),
        ('N', 'When needed')
    )
    # CharField() limits the number of characters, while TextField() doesn't
    task = models.CharField(max_length=255)
    instructions = models.TextField()
    frequence = models.CharField(max_length=2, choices=frequence_choices, default='D')

    def __str__(self):
        return self.task
    
class Consultations(models.Model):
    mood = models.PositiveIntegerField()
    general_registration = models.TextField()
    video = models.FileField(upload_to="video")
    tasks = models.ManyToManyField(Tasks)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE) # CASCADE = if the patient from the consultation was excluded delete this patient's consultations
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient.name

    @property
    def public_link(self):
        return f"http://127.0.0.1:8000{reverse('public_consultation', kwargs={'id': self.id})}"
