from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app_clinica/', include('app_clinica.urls')),
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
