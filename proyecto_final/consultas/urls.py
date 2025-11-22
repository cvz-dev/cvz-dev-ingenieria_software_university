from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_consultas, name="menu_consultas"),

    path("prerrequisitos/", views.consulta_prerrequisitos, name="consulta1"),
    path("transcript/", views.consulta_transcript, name="consulta2"),
    path("asesor/", views.consulta_estudiante_asesor, name="consulta3"),
    path("estudiantes-A/", views.consulta_estudiantes_A, name="consulta4"),
    path("cursos-profesor/", views.consulta_cursos_profesor, name="consulta5"),
]
