from django.urls import path
from . import views

urlpatterns = [
    path('', views.pacientes, name="patients"),
    path('<int:id>', views.paciente_view, name="patient_view"),
    path('update_patient/<int:id>', views.update_patient, name="update_patient"),
    path('delete_consultation/<int:id>', views.delete_consultation, name="delete_consultation"),
    path('public_consultation/<int:id>', views.public_consultation, name="public_consultation"),
    path('cadastrar_terapeuta/', views.cadastrar_terapeuta, name='cadastrar_terapeuta'),
]