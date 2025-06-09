from django.contrib import admin
from .models import Patients, Therapist, Treatment

admin.site.register(Patients)
admin.site.register(Therapist)
admin.site.register(Treatment)
admin.site.site_header = 'Sistema de Gestão Clínica'
admin.site.site_title = 'Administração do Sistema de Gestão Clínica'
admin.site.index_title = 'Painel de Controle'

