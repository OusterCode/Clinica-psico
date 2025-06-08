from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name="index"),
    path('pacientes/', views.pacientes, name="patients"),
    path('pacientes/<int:id>', views.paciente_view, name="patient_view"),
    path('pacientes/update_patient/<int:id>', views.update_patient, name="update_patient"),
    path('consultas/delete_consultation/<int:id>', views.delete_consultation, name="delete_consultation"),
    path('consultas/public_consultation/<int:id>', views.public_consultation, name="public_consultation"),
    path('terapeutas/cadastrar_terapeuta/', views.cadastrar_terapeuta, name='cadastrar_terapeuta'),
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('logout/', views.logout_view, name='logout'),
    path('pacientes_cadastrados/', views.pacientes_cadastrados, name='pacientes_cadastrados'),
]

# Nenhuma alteração necessária aqui, pois as views já estão protegidas por login_required.