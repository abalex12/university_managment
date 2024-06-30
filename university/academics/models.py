from django.db import models
from userauth.models import User, Student, Teacher
from shortuuid.django_fields import ShortUUIDField
class Year(models.Model):
    year_id = ShortUUIDField(length=7, prefix='year', primary_key=True)
    year_name = models.CharField(max_length=20)
     
    def __str__(self):
        return self.year_name

class AcademicYear(models.Model):
    academic_year_id = ShortUUIDField(length=7, prefix='Aca', primary_key=True)
    academic_year_name = models.CharField(max_length=20)
    academic_Semester=models.CharField(max_length=10, choices=[('Fall', 'Fall'),('Winter', 'Winter')], null=True, blank=True)
    def __str__(self):
        return self.academic_year_name

class Semester(models.Model):
    semester_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Sem", alphabet="1234567890", primary_key=True)
    semester_name = models.CharField(max_length=100)

    def __str__(self):
        return self.semester_name

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

class SemesterYear(models.Model):
    semester_year_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="SemY", alphabet="1234567890", primary_key=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, related_name='semester_years', null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"{self.semester.semester_name} {self.academic_year.academic_year_name}"

    class Meta:
        unique_together = ('semester', 'academic_year')
        verbose_name = "Semester Year"
        verbose_name_plural = "Semester Years"

class Course(models.Model):
    course_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Cour", alphabet="1234567890", primary_key=True)
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    credit_hours = models.PositiveIntegerField()

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        

class Department(models.Model):
    department_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Dep", alphabet="1234567890", primary_key=True)
    department_name = models.CharField(max_length=100)
    head_of_department = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True ,related_name='Department')
    description = models.CharField(max_length=255, null=True, blank=True)
    office_location = models.CharField(max_length=255, null=True, blank=True)
    course=models.ManyToManyField(Course)

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"



class CourseSemesterAvailability(models.Model):
    course_semester_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="CourS", alphabet="1234567890")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_semester_availabilities')
    semester_year = models.ForeignKey(SemesterYear, on_delete=models.CASCADE, related_name='course_semester_availabilities')
    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name="CourseSemesterAvailability")

    class Meta:
        unique_together = ('course', 'semester_year','department')
        verbose_name = "Course Semester Availability"
        verbose_name_plural = "Course Semester Availabilities"

    def __str__(self):
        return f"{self.course.course_name} - {self.semester_year}"

class Enrollment(models.Model):
    enrollment_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Enro", alphabet="1234567890", primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course_semester = models.ForeignKey(CourseSemesterAvailability, on_delete=models.CASCADE, related_name='enrollments')
    registration_date = models.DateTimeField(auto_now_add=True)
    retake = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course_semester')
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.student} enrolled in {self.course_semester}"

class Section(models.Model):
    section_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Sec", alphabet="1234567890", primary_key=True)
    section_name = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return f"{self.section_name}-{self.department}"
    
    class Meta:
        unique_together = ('section_id', 'section_name', 'department')
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

class TeacherCourse(models.Model):
    teacher_course_id = ShortUUIDField(unique=True, length=5, max_length=10, prefix="Teac", alphabet="1234567890", primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_courses')
    course_semester = models.ForeignKey(CourseSemesterAvailability, on_delete=models.CASCADE, related_name='teacher_courses')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='teacher_courses')

    def __str__(self):
        return f"{self.teacher} - {self.course_semester}"
    class Meta:
        unique_together=('course_semester','section')
