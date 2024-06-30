from django.contrib import admin
from .models import (
    Year, AcademicYear, Semester, SemesterYear, Department, 
    Course, CourseSemesterAvailability, Enrollment, Section, TeacherCourse
)

@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ('year_id', 'year_name')
    search_fields = ('year_name',)

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('academic_year_id', 'academic_year_name')
    search_fields = ('academic_year_name',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester_id', 'semester_name')
    search_fields = ('semester_name',)

@admin.register(SemesterYear)
class SemesterYearAdmin(admin.ModelAdmin):
    list_display = ('semester_year_id', 'semester', 'academic_year', 'start_date', 'end_date')
    list_filter = ('semester', 'academic_year')
    search_fields = ('semester__semester_name', 'academic_year__academic_year_name')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name', 'head_of_department', 'office_location')
    list_filter = ('head_of_department',)
    search_fields = ('department_name', 'office_location')
    filter_horizontal=('course',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name', 'course_code', 'credit_hours')
    list_filter = ('course_name',)
    search_fields = ('course_name', 'course_code')
    

@admin.register(CourseSemesterAvailability)
class CourseSemesterAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('course_semester_id', 'course', 'semester_year')
    list_filter = ('course', 'semester_year')
    search_fields = ('course__course_name', 'semester_year__semester__semester_name', 'semester_year__academic_year__academic_year_name')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_id', 'student', 'course_semester', 'registration_date', 'retake')
    list_filter = ('retake', 'registration_date')
    search_fields = ('student__name', 'course_semester__course__course_name', 'course_semester__semester_year__semester__semester_name')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'section_name', 'department')
    list_filter = ('department',)
    search_fields = ('section_name', 'department__department_name')

@admin.register(TeacherCourse)
class TeacherCourseAdmin(admin.ModelAdmin):
    list_display = ('teacher_course_id', 'teacher', 'course_semester', 'section')
    list_filter = ('teacher', 'course_semester', 'section')
    search_fields = ('teacher__name', 'course_semester__course__course_name', 'section__section_name')
