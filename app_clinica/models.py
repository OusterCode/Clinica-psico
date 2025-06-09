from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# =========================
# Modelos Abstratos
# =========================

class AbstractPerson(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField(verbose_name='Data de Nascimento')
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    CEP = models.CharField(max_length=8, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        abstract = True

# =========================
# Choices e Modelos Auxiliares
# =========================

TREATMENT_CHOICES = [
    ('ADHD', 'ADHD'),
    ('D', 'Depressão'),
    ('A', 'Ansiedade'),
    ('GAD', 'Transtorno de ansiedade generalizada'),
    ("Terapia", 'Terapia'),
    ('TCC', 'Terapia Cognitivo-Comportamental'),
    ('Fobia', 'Fobia Social'),
    ('TOC', 'Transtorno Obsessivo-Compulsivo'),
    ('PTSD', 'Transtorno de Estresse Pós-Traumático'),
    ('Outros', 'Outros')
]

class Treatment(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

# Popula tratamentos após migração
@receiver(post_migrate)
def populate_treatments(sender, **kwargs):
    if sender.name.endswith('app_clinica'):
        for code, desc in TREATMENT_CHOICES:
            Treatment.objects.get_or_create(code=code, description=desc)

# =========================
# Modelos Principais
# =========================

class Patients(AbstractPerson):
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tratamento')
    payment_on_day = models.BooleanField(default=True)

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/media/pessoa_logo.jpeg'

    def __str__(self):
        return self.name

class Therapist(AbstractPerson):
    degree = models.CharField(max_length=255, verbose_name='Grau de formação')
    treatments = models.ManyToManyField(Treatment, verbose_name='Tratamentos que pode ministrar')
    is_subleasing = models.BooleanField(default=False, verbose_name='Subloca consultório?')
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Valor da hora')
    available_days = models.CharField(max_length=100, verbose_name='Dias disponíveis')
    available_times = models.CharField(max_length=100, verbose_name='Horários disponíveis')

    def __str__(self):
        return self.name

    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        return '/media/pessoa_logo.jpeg'

class Agendamento(models.Model):
    data = models.DateField()
    hora = models.TimeField()
    terapeuta = models.ForeignKey('Therapist', on_delete=models.CASCADE)
    paciente = models.ForeignKey('Patients', on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True)
    cor = models.CharField(max_length=7, default="#4285F4")  # cor HEX para o terapeuta
    duracao = models.PositiveIntegerField(default=50, verbose_name='Duração da sessão (minutos)')

    def __str__(self):
        return f"{self.data} {self.hora} - {self.paciente.name} ({self.terapeuta.name})"