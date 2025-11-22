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
        null=True
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
        null=True
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
        null=True
    )
    tot_cred = models.IntegerField()

    class Meta:
        db_table = "student"

    def __str__(self):
        return self.name


# -------------------------------------------------
# CLASSROOM (sin FK en Section)
# -------------------------------------------------
class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    building = models.CharField(max_length=15)
    room_number = models.CharField(max_length=7)
    capacity = models.IntegerField()

    class Meta:
        db_table = "classroom"
        unique_together = ("building", "room_number")

    def __str__(self):
        return f"{self.building} {self.room_number}"


# -------------------------------------------------
# TIME SLOT (sin FK directo en Section)
# -------------------------------------------------
class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True)
    time_slot_id = models.CharField(max_length=4)  # A/B/C etc.
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
# SECTION (solo FK a Course)
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

    # Campos heredados sin FK
    building = models.CharField(max_length=15)
    room_number = models.CharField(max_length=7)
    time_slot_id = models.CharField(max_length=4)

    class Meta:
        db_table = "section"
        unique_together = ("course", "sec_id", "semester", "year")

    def __str__(self):
        return f"{self.course_id} Sec {self.sec_id} ({self.semester} {self.year})"


# -------------------------------------------------
# TEACHES (FK a Instructor y Section)
# -------------------------------------------------
class Teaches(models.Model):
    id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(
        Instructor,
        to_field="ID",
        db_column="instructor_id",
        on_delete=models.CASCADE
    )
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=8)
    semester = models.CharField(max_length=6)
    year = models.IntegerField()

    class Meta:
        db_table = "teaches"

    def __str__(self):
        return f"{self.instructor} teaches {self.course_id}"


# -------------------------------------------------
# TAKES (FK a Student)
# -------------------------------------------------
class Takes(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student,
        to_field="ID",
        db_column="student_id",
        on_delete=models.CASCADE
    )
    course_id = models.CharField(max_length=8)
    sec_id = models.CharField(max_length=8)
    semester = models.CharField(max_length=6)
    year = models.IntegerField()
    grade = models.CharField(max_length=2, null=True)

    class Meta:
        db_table = "takes"

    def __str__(self):
        return f"{self.student} - {self.course_id}"


# -------------------------------------------------
# ADVISOR
# -------------------------------------------------
class Advisor(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
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
        null=True
    )

    class Meta:
        db_table = "advisor"
        unique_together = ("student", "instructor")

    def __str__(self):
        return f"{self.student} advised by {self.instructor}"


# -------------------------------------------------
# PREREQ
# -------------------------------------------------
class Prereq(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course,
        to_field="course_id",
        db_column="course_id",
        on_delete=models.CASCADE
    )
    prereq = models.ForeignKey(
        Course,
        to_field="course_id",
        db_column="prereq_id",
        related_name="prerequisites",
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "prereq"
        unique_together = ("course", "prereq")

    def __str__(self):
        return f"{self.prereq} → {self.course}"
