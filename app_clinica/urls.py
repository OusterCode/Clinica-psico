from django.urls import path
from . import views

urlpatterns = [
    # Rotas de autenticação e boas-vindas
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('welcome/', views.welcome, name='welcome'),
    path('', views.welcome, name="index"),  # Página inicial redireciona para welcome

    # Rotas de pacientes
    path('pacientes/cadastrar_paciente/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('pacientes/visualizar_pacientes/', views.visualizar_pacientes, name='visualizar_pacientes'),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/excluir/<int:id>/', views.excluir_paciente, name='excluir_paciente'),

    # Rotas de terapeutas
    path('terapeutas/cadastrar_terapeuta/', views.cadastrar_terapeuta, name='cadastrar_terapeuta'),
    path('terapeutas/visualizar_terapeutas/', views.visualizar_terapeutas, name='visualizar_terapeutas'),
    path('terapeutas/editar/<int:id>/', views.editar_terapeuta, name='editar_terapeuta'),
    path('terapeutas/excluir/<int:id>/', views.excluir_terapeuta, name='excluir_terapeuta'),
]

# As views sensíveis já estão protegidas por login_required no arquivo de views.