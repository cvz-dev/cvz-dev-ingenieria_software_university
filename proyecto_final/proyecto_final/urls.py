# _project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirigir la raíz (/) al menú de consultas
    path('', lambda request: redirect('menu_consultas'), name='home'),
    path('consultas/', include('consultas.urls')),
]