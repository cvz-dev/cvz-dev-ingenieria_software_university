from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
from .models import (
    Course, Student, Instructor,
    Prereq, Takes, Advisor, Teaches
)

# -------------------------------------------------
# MENÚ GENERAL DE CONSULTAS
# -------------------------------------------------
def menu_consultas(request):
    return render(request, "consultas/menu.html")


# -------------------------------------------------
# CONSULTA 1: Prerrequisitos de un curso
# -------------------------------------------------
def consulta_prerrequisitos(request):
    course_id = request.GET.get("course_id")
    resultado = []
    curso = None

    if course_id:
        curso = Course.objects.filter(course_id=course_id).first()
        resultado = Prereq.objects.filter(course__course_id=course_id).select_related("prereq")

    return render(request, "consultas/consulta1.html", {
        "course_id": course_id,
        "curso": curso,
        "resultado": resultado
    })


# -------------------------------------------------
# CONSULTA 2: Transcript de un estudiante
# -------------------------------------------------
def consulta_transcript(request):
    student_id = request.GET.get("student_id")
    resultado = []
    estudiante = None

    if student_id:
        estudiante = Student.objects.filter(ID=student_id).first()
        resultado = Takes.objects.filter(student__ID=student_id).select_related("student")

    return render(request, "consultas/consulta2.html", {
        "student_id": student_id,
        "estudiante": estudiante,
        "resultado": resultado
    })


# -------------------------------------------------
# CONSULTA 3: Estudiante y su asesor
# -------------------------------------------------
def consulta_estudiante_asesor(request):
    student_id = request.GET.get("student_id")
    resultado = []
    estudiante = None

    if student_id:
        estudiante = Student.objects.filter(ID=student_id).first()
        resultado = Advisor.objects.filter(student__ID=student_id).select_related("student", "instructor")

    return render(request, "consultas/consulta3.html", {
        "student_id": student_id,
        "estudiante": estudiante,
        "resultado": resultado
    })


# -------------------------------------------------
# CONSULTA 4: Estudiantes con 'A' en un curso
# -------------------------------------------------
def consulta_estudiantes_A(request):
    course_id = request.GET.get("course_id")
    resultado = []

    if course_id:
        resultado = Takes.objects.filter(course_id=course_id, grade="A").select_related("student")

    return render(request, "consultas/consulta4.html", {
        "course_id": course_id,
        "resultado": resultado
    })


# -------------------------------------------------
# CONSULTA 5: Cursos impartidos por un profesor
# -------------------------------------------------
def consulta_cursos_profesor(request):
    instructor_id = request.GET.get("instructor_id")
    resultado = []
    profesor = None

    if instructor_id:
        profesor = Instructor.objects.filter(ID=instructor_id).first()
        resultado = Teaches.objects.filter(instructor__ID=instructor_id).select_related("instructor")

    return render(request, "consultas/consulta5.html", {
        "instructor_id": instructor_id,
        "profesor": profesor,
        "resultado": resultado
    })
