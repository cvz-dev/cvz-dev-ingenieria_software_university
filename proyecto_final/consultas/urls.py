from django.urls import path
from . import views

urlpatterns = [
    path('estudiantes/', views.listar_estudiantes, name='listar_estudiantes'),
]