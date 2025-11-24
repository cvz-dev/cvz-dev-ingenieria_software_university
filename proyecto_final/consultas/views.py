from django.shortcuts import render
from .models import (
    Course, Student, Instructor,
    Prereq, Takes, Advisor, Teaches,
)

# -------------------------------------------------
# MENÚ PRINCIPAL
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

    # Lista de cursos para el select
    cursos = Course.objects.all().order_by("course_id")

    if course_id:
        curso = Course.objects.filter(course_id=course_id).first()
        resultado = Prereq.objects.filter(
            course__course_id=course_id
        ).select_related("prereq", "course")

    return render(request, "consultas/consulta1.html", {
        "course_id": course_id,
        "curso": curso,
        "resultado": resultado,
        "cursos": cursos,
    })


# -------------------------------------------------
# CONSULTA 2: Transcript de un estudiante
# -------------------------------------------------
def consulta_transcript(request):
    student_id = request.GET.get("student_id")
    resultado = []
    estudiante = None

    # Lista dinámica de estudiantes
    estudiantes = Student.objects.all().order_by("ID")

    if student_id:
        estudiante = Student.objects.filter(ID=student_id).first()
        # CAMBIO: ahora usa section__course para acceder al curso
        resultado = Takes.objects.filter(
            student__ID=student_id
        ).select_related(
            "student",
            "section",
            "section__course"
        ).order_by(
            "section__year",
            "section__semester"
        )

    return render(request, "consultas/consulta2.html", {
        "student_id": student_id,
        "estudiante": estudiante,
        "resultado": resultado,
        "estudiantes": estudiantes,
    })


# -------------------------------------------------
# CONSULTA 3: Estudiante y su asesor
# -------------------------------------------------
def consulta_estudiante_asesor(request):
    student_id = request.GET.get("student_id")
    resultado = None
    estudiante = None

    # Select con todos los estudiantes
    estudiantes = Student.objects.all().order_by("ID")

    if student_id:
        estudiante = Student.objects.filter(ID=student_id).first()
        # CAMBIO: ahora Advisor es OneToOne, así que usamos .first() o try/except
        try:
            resultado = Advisor.objects.select_related(
                "student",
                "instructor"
            ).get(student__ID=student_id)
        except Advisor.DoesNotExist:
            resultado = None

    return render(request, "consultas/consulta3.html", {
        "student_id": student_id,
        "estudiante": estudiante,
        "resultado": resultado,
        "estudiantes": estudiantes,
    })


# -------------------------------------------------
# CONSULTA 4: Estudiantes con 'A' en un curso
# -------------------------------------------------
def consulta_estudiantes_A(request):
    course_id = request.GET.get("course_id")
    resultado = []

    # Todos los cursos para el menú
    cursos = Course.objects.all().order_by("course_id")

    if course_id:
        # CAMBIO: ahora filtramos por section__course__course_id
        resultado = Takes.objects.filter(
            section__course__course_id=course_id,
            grade = "A "
        ).select_related(
            "student",
            "section",
            "section__course"
        ).order_by("student__name")

    return render(request, "consultas/consulta4.html", {
        "course_id": course_id,
        "resultado": resultado,
        "cursos": cursos,
    })


# -------------------------------------------------
# CONSULTA 5: Cursos impartidos por un profesor
# -------------------------------------------------
def consulta_cursos_profesor(request):
    instructor_id = request.GET.get("instructor_id")
    resultado = []
    profesor = None

    # Lista de instructores para el select
    profesores = Instructor.objects.all().order_by("ID")

    if instructor_id:
        profesor = Instructor.objects.filter(ID=instructor_id).first()
        # CAMBIO: ahora accedemos al curso a través de section
        resultado = Teaches.objects.filter(
            instructor__ID=instructor_id
        ).select_related(
            "instructor",
            "section",
            "section__course"
        ).order_by(
            "section__year",
            "section__semester"
        )

    return render(request, "consultas/consulta5.html", {
        "instructor_id": instructor_id,
        "profesor": profesor,
        "resultado": resultado,
        "profesores": profesores,
    })