from django.shortcuts import render
from .models import (
    Course, Student, Instructor,
    Prereq, Takes, Advisor, Teaches, Section
)

# Función para limpiar la consulta SQL
def clean_sql(queryset):
    sql = str(queryset.query)
    sql = sql.replace('"', '').replace("`", "")
    sql = sql.replace('SELECT', 'SELECT ')
    sql = sql.replace('FROM', '\nFROM')
    sql = sql.replace('WHERE', '\nWHERE')
    sql = sql.replace('INNER JOIN', '\nINNER JOIN')
    sql = sql.replace('ORDER BY', '\nORDER BY')
    return sql

# MENÚ PRINCIPAL
def menu_consultas(request):
    return render(request, "consultas/menu.html")

# CONSULTA 1
def consulta_prerrequisitos(request):
    course_id = request.GET.get("course_id")
    resultado = []
    curso = None
    sql_query = None

    cursos = Course.objects.all().order_by("course_id")

    if course_id:
        curso = Course.objects.filter(course_id=course_id).first()
        qs = Prereq.objects.filter(course__course_id=course_id).select_related("prereq", "course")
        sql_query = clean_sql(qs)
        resultado = qs

    return render(request, "consultas/consulta1.html", {
        "course_id": course_id, "curso": curso, "resultado": resultado, "cursos": cursos, "sql_query": sql_query
    })

# CONSULTA 2
def consulta_transcript(request):
    student_id = request.GET.get("student_id")
    resultado = []
    estudiante = None
    sql_query = None

    estudiantes = Student.objects.all().order_by("ID")

    if student_id:
        estudiante = Student.objects.filter(ID=student_id).first()
        qs = Takes.objects.filter(student__ID=student_id).select_related("section", "section__course")
        sql_query = clean_sql(qs)
        resultado = qs

    return render(request, "consultas/consulta2.html", {
        "student_id": student_id, "estudiante": estudiante, "resultado": resultado, "estudiantes": estudiantes, "sql_query": sql_query
    })

# CONSULTA 3
def consulta_estudiante_asesor(request):
    student_id = request.GET.get("student_id")
    resultado = None
    estudiante = None
    sql_query = None

    estudiantes = Student.objects.all().order_by("ID")

    if student_id:
        estudiante = Student.objects.filter(ID=student_id).first()
        qs = Advisor.objects.filter(student__ID=student_id).select_related("student", "instructor")
        sql_query = clean_sql(qs)
        resultado = qs.first()

    return render(request, "consultas/consulta3.html", {
        "student_id": student_id, "estudiante": estudiante, "resultado": resultado, "estudiantes": estudiantes, "sql_query": sql_query
    })

# CONSULTA 4
def consulta_estudiantes_A(request):
    course_id = request.GET.get("course_id")
    resultado = []
    sql_query = None

    cursos = Course.objects.all().order_by("course_id")

    if course_id:
        qs = Takes.objects.filter(section__course__course_id=course_id, grade="A ").select_related("student", "section", "section__course").order_by("student__name")
        sql_query = clean_sql(qs)
        resultado = qs

    return render(request, "consultas/consulta4.html", {
        "course_id": course_id, "resultado": resultado, "cursos": cursos, "sql_query": sql_query
    })

# CONSULTA 5
def consulta_cursos_profesor(request):
    instructor_id = request.GET.get("instructor_id")
    resultado = []
    profesor = None
    sql_query = None
    
    profesores = Instructor.objects.all().order_by("ID")

    if instructor_id:
        profesor = Instructor.objects.filter(ID=instructor_id).first()
        qs = Teaches.objects.filter(instructor__ID=instructor_id).select_related("instructor", "section", "section__course").order_by("section__year", "section__semester")
        sql_query = clean_sql(qs)
        resultado = qs

    return render(request, "consultas/consulta5.html", {
        "instructor_id": instructor_id, "profesor": profesor, "resultado": resultado, "profesores": profesores, "sql_query": sql_query
    })