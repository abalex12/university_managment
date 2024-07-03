from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Enrollment, TeacherCourse,CourseSemesterAvailability,Course
from userauth.models import Student ,User,Teacher
from .forms import *
from django.contrib import messages

@login_required
def display_detail(request):
    user = request.user
    role_name = user.role.role_name if user.role else None

    if role_name == "Student":
        student_profile = get_object_or_404(Student, user=user)
        context = {
            'user_profile': user,
            'profile': student_profile,
        }
        return render(request, "academics/details.html", context)
    elif role_name == "Teacher":
        teacher_profile = get_object_or_404(Teacher, user=user)
        context = {
            'user_profile': user,
            'profile': teacher_profile,
        }
        return render(request, "academics/details.html", context)
    # elif role_name == "Admin":
    #     admin_profile = get_object_or_404(Admin, user=user)
    #     context = {
    #         'user_profile': user,
    #         'profile': admin_profile,
    #     }
    #     return render(request, "academics/admin_details.html", context)
    else:
        return render(request, "academics/unknown_role.html")
    

@login_required
def course_registration(request):
    user = request.user
    student_profile = get_object_or_404(Student, user=user)

    # the student's current semester year is stored in a field `current_semester_year`
    current_semester_year = student_profile.semester
    department = student_profile.department

    if not current_semester_year:
        return HttpResponse("No current semester year found.")

    # Get available courses for the student's current semester year
    available_courses = CourseSemesterAvailability.objects.filter(
        semester_year=current_semester_year, 
        department = department
    )

    enrolled_courses = Enrollment.objects.filter(
        student=student_profile, 
        course_semester__semester_year=current_semester_year
    )
    enrolled_course_ids = enrolled_courses.values_list('course_semester_id', flat=True)
    success = False

    if request.method == 'POST':
        course_semester_ids = request.POST.getlist('course_semester_ids')
        for course_semester_id in course_semester_ids:
            course_semester = CourseSemesterAvailability.objects.get(id=course_semester_id)

            # Create an enrollment if not already enrolled
            if not Enrollment.objects.filter(student=student_profile, course_semester=course_semester).exists():
                Enrollment.objects.create(student=student_profile, course_semester=course_semester)

        success = True

    context = {
        'user_profile': user,
        'profile': student_profile,
        'available_courses': available_courses, 
        'enrolled_course_ids': enrolled_course_ids,
        'success': success,
    }

    return render(request, 'academics/course_registration.html', context)

@login_required
def edit_profile(request):
    user = request.user
    user_form = UserProfileForm(instance=user)
    student_form = None
    teacher_form = None

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        if user.role.role_name == "Student":
            student_profile = get_object_or_404(Student, user=user)
            student_form = StudentDetailsForm(request.POST, instance=student_profile)

            for field in ['first_name', 'last_name', 'username', 'date_of_birth']:
                user_form.fields[field].disabled = True
            
            for field in ['semester', 'department', 'section','year']:
                student_form.fields[field].disabled = True

            if user_form.is_valid():
                user_form.save()
                if student_form.is_valid():
                    
                    # Retain the original gender and profile picture if not provided
                    student_profile = student_form.save(commit=False)
                    # student_profile.gender = user.gender
                    if 'profile_picture' in request.FILES:
                        user.profile_picture = request.FILES['profile_picture']
                    else:
                        user.profile_picture = user_form.initial['profile_picture']
                    student_profile.save()
                    messages.success(request, 'Profile updated successfully.')
                    return redirect('academics:detail')
                else:
                    print(student_form.errors)
            else:
                # print(teacher_form.errors)
                messages.error(request, 'Please correct the errors below.')
        
        elif user.role.role_name == "Teacher":
            teacher_profile = get_object_or_404(Teacher, user=user)
            teacher_form = TeacherDetailsForm(request.POST, instance=teacher_profile)

            for field in ['first_name', 'last_name', 'username', 'date_of_birth','gender']:
                user_form.fields[field].disabled = True
            
            for field in ['qualifications', 'department','office_hours' ]:
                teacher_form.fields[field].disabled = True

            if user_form.is_valid():
                
                user_form.save()
                if teacher_form.is_valid():
                    teacher_profile = teacher_form.save(commit=False)
                    # teacher_profile.gender = user.gender
                    if 'profile_picture' in request.FILES:
                        user.profile_picture = request.FILES['profile_picture']
                    else:
                        user.profile_picture = user_form.initial['profile_picture']
                    teacher_profile.save()
              
                    messages.success(request, 'Profile updated successfully.')
                   
                    return redirect('academics:detail')
                else:
                    print(teacher_form.errors)
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        if user.role.role_name == "Student":
            student_profile = get_object_or_404(Student, user=user)
            student_form = StudentDetailsForm(instance=student_profile)
        

        elif user.role.role_name == "Teacher":
            teacher_profile = get_object_or_404(Teacher, user=user)
            teacher_form = TeacherDetailsForm(instance=teacher_profile)
        

    context = {
        'user_form': user_form,
        'student_form': student_form,
        'teacher_form': teacher_form,
    }

    return render(request, 'academics/edit_detail.html', context)

@login_required
def open_sections(reqeust):
    return render(reqeust,'academics/teacher_sections.html')
    