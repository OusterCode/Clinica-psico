from django.db import models
from django.urls import reverse
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class AbstractPerson(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField(verbose_name='Data de Nascimento')
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    CEP = models.CharField(max_length=8, null=True, blank=True)  # CEP is a Brazilian postal code
    address = models.CharField(max_length=255, null=True, blank=True)  # Full address
    city = models.CharField(max_length=255, null=True, blank=True)  # City
    state = models.CharField(max_length=2, null=True, blank=True)  # State (e.g., SP for São Paulo)
    numero = models.CharField(max_length=10, null=True, blank=True)  # Número do endereço (casa, apto, etc.)

    class Meta:
        abstract = True

class Patients(AbstractPerson):
    complaint_choices = (
        ('ADHD', 'ADHD'),
        ('D', 'Depressão'),
        ('A', 'Ansiedade'),
        ('GAD', 'Transtorno de ansiedade generalizada'),
        ("Terapia", 'Terapia de Casal'),
        ('TCC', 'Terapia Cognitivo-Comportamental'),
        ('Fobia', 'Fobia Social'),
        ('TOC', 'Transtorno Obsessivo-Compulsivo'),
        ('PTSD', 'Transtorno de Estresse Pós-Traumático'),
        ('Outros', 'Outros')
    )
    complaint = models.CharField(max_length=7, choices=complaint_choices, default='ADHD')
    payment_on_day = models.BooleanField(default=True)
    
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/media/pessoa_logo.jpeg'

    # Magic method
    def __str__(self):
        return self.name
    
class Tasks(models.Model):
    frequence_choices = (
        ('D', 'Diário'),
        ('1S', '1 vez por semana'),
        ('2S', '2 vezes por semana'),
        ('3S', '3 vezes por semana'),
        ('1M', '1 vez por mês'),
        ('2M', '2 vezes por mês'),
        ('N', 'Quando necessário')
    )
    # CharField() limits the number of characters, while TextField() doesn't
    task = models.CharField(max_length=255)
    instructions = models.TextField()
    frequence = models.CharField(max_length=2, choices=frequence_choices, default='1S')

    def __str__(self):
        return self.task
    
class Consultations(models.Model):
    mood = models.PositiveIntegerField()
    general_registration = models.TextField()
    video = models.FileField(upload_to="video")
    tasks = models.ManyToManyField(Tasks)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE) # CASCADE = if the patient from the consultation was excluded delete this patient's consultations
    date = models.DateTimeField(auto_now_add=True)
    valor_da_sessao = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Value of the session in BRL

    def __str__(self):
        return self.patient.name

    @property
    def public_link(self):
        return f"http://127.0.0.1:8000{reverse('public_consultation', kwargs={'id': self.id})}"
    
class Therapist(AbstractPerson):
    degree = models.CharField(max_length=255, verbose_name='Grau de formação')
    complaints = models.ManyToManyField('Complaint', verbose_name='Queixas que pode tratar')
    is_subleasing = models.BooleanField(default=False, verbose_name='Subloca consultório?')
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Valor da hora')
    available_days = models.CharField(max_length=100, verbose_name='Dias disponíveis')  # Ex: Segunda, Terça
    available_times = models.CharField(max_length=100, verbose_name='Horários disponíveis')  # Ex: 08:00-12:00, 14:00-18:00

    def __str__(self):
        return self.name

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/media/pessoa_logo.jpeg'

class Complaint(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

# complaint_choices já existe, vamos popular Complaint automaticamente
@receiver(post_migrate)
def populate_complaints(sender, **kwargs):
    from .models import Complaint, Patients
    if sender.name == 'patients':
        for code, desc in Patients.complaint_choices:
            Complaint.objects.get_or_create(code=code, description=desc)
