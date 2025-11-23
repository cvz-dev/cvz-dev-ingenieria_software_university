from django.db import models


# -------------------------------------------------
# DEPARTMENT
# -------------------------------------------------
class Department(models.Model):
    dept_name = models.CharField(max_length=20, primary_key=True)
    building = models.CharField(max_length=15, null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "department"

    def __str__(self):
        return self.dept_name


# -------------------------------------------------
# COURSE
# -------------------------------------------------
class Course(models.Model):
    course_id = models.CharField(max_length=8, primary_key=True)
    title = models.CharField(max_length=50)
    dept_name = models.ForeignKey(
        Department,
        to_field="dept_name",
        db_column="dept_name",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    credits = models.IntegerField()

    class Meta:
        db_table = "course"

    def __str__(self):
        return f"{self.course_id} - {self.title}"


# -------------------------------------------------
# INSTRUCTOR
# -------------------------------------------------
class Instructor(models.Model):
    ID = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=20)
    dept_name = models.ForeignKey(
        Department,
        to_field="dept_name",
        db_column="dept_name",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    salary = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "instructor"

    def __str__(self):
        return self.name


# -------------------------------------------------
# STUDENT
# -------------------------------------------------
class Student(models.Model):
    ID = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=20)
    dept_name = models.ForeignKey(
        Department,
        to_field="dept_name",
        db_column="dept_name",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tot_cred = models.IntegerField()

    class Meta:
        db_table = "student"

    def __str__(self):
        return self.name


# -------------------------------------------------
# CLASSROOM (CORREGIDO: ahora Section tiene FK a esta tabla)
# -------------------------------------------------
class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    building = models.CharField(max_length=15)
    room_number = models.CharField(max_length=7)
    capacity = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "classroom"
        unique_together = ("building", "room_number")

    def __str__(self):
        return f"{self.building} {self.room_number}"


# -------------------------------------------------
# TIME SLOT (sin cambios, pero ahora no se usa directamente)
# -------------------------------------------------
class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True)
    time_slot_id = models.CharField(max_length=4)
    day = models.CharField(max_length=1)
    start_hr = models.IntegerField()
    start_min = models.IntegerField()
    end_hr = models.IntegerField()
    end_min = models.IntegerField()

    class Meta:
        db_table = "time_slot"
        unique_together = ("time_slot_id", "day", "start_hr", "start_min")

    def __str__(self):
        return f"{self.time_slot_id} ({self.day})"


# -------------------------------------------------
# SECTION (CORREGIDO: ahora con FK a Classroom)
# -------------------------------------------------
class Section(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course,
        to_field="course_id",
        db_column="course_id",
        on_delete=models.CASCADE
    )
    sec_id = models.CharField(max_length=8)
    semester = models.CharField(max_length=6)
    year = models.IntegerField()
    
    # CAMBIO IMPORTANTE: ahora es FK a Classroom
    classroom = models.ForeignKey(
        Classroom,
        db_column="classroom_id",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Este campo se mantiene como CharField (sin FK)
    time_slot_id = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        db_table = "section"
        unique_together = ("course", "sec_id", "semester", "year")

    def __str__(self):
        return f"{self.course_id} Sec {self.sec_id} ({self.semester} {self.year})"


# -------------------------------------------------
# TEACHES (CORREGIDO: ahora con FK a Section)
# -------------------------------------------------
class Teaches(models.Model):
    id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(
        Instructor,
        to_field="ID",
        db_column="instructor_id",
        on_delete=models.CASCADE
    )
    # CAMBIO IMPORTANTE: ahora es FK a Section
    section = models.ForeignKey(
        Section,
        db_column="section_id",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "teaches"
        unique_together = ("instructor", "section")

    def __str__(self):
        return f"{self.instructor} teaches {self.section}"


# -------------------------------------------------
# TAKES (CORREGIDO: ahora con FK a Section)
# -------------------------------------------------
class Takes(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student,
        to_field="ID",
        db_column="student_id",
        on_delete=models.CASCADE
    )
    # CAMBIO IMPORTANTE: ahora es FK a Section
    section = models.ForeignKey(
        Section,
        db_column="section_id",
        on_delete=models.CASCADE
    )
    grade = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        db_table = "takes"
        unique_together = ("student", "section")

    def __str__(self):
        return f"{self.student} - {self.section}"


# -------------------------------------------------
# ADVISOR (CORREGIDO: unique solo en student)
# -------------------------------------------------
class Advisor(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.OneToOneField(  # CAMBIO: OneToOne en vez de ForeignKey
        Student,
        to_field="ID",
        db_column="s_ID",
        on_delete=models.CASCADE
    )
    instructor = models.ForeignKey(
        Instructor,
        to_field="ID",
        db_column="i_ID",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "advisor"
        # No necesita unique_together porque student es OneToOne

    def __str__(self):
        return f"{self.student} advised by {self.instructor}"


# -------------------------------------------------
# PREREQ (sin cambios significativos)
# -------------------------------------------------
class Prereq(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course,
        to_field="course_id",
        db_column="course_id",
        on_delete=models.CASCADE,
        related_name="prereq_for"
    )
    prereq = models.ForeignKey(
        Course,
        to_field="course_id",
        db_column="prereq_id",
        related_name="is_prereq_of",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "prereq"
        unique_together = ("course", "prereq")

    def __str__(self):
        return f"{self.prereq} → {self.course}"