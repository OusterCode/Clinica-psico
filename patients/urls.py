from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients, name="patients"),
    path('<int:id>', views.patient_view, name="patient_view"),
    path('update_patient/<int:id>', views.update_patient, name="update_patient"),
    path('delete_consultation/<int:id>', views.delete_consultation, name="delete_consultation"),
    path('public_consultation/<int:id>', views.public_consultation, name="public_consultation"),
]