from django.utils import timezone
from django.shortcuts import get_object_or_404
from academics.models import TeacherCourse, Enrollment, AcademicYear, CourseSemesterAvailability
from assessment.models import Quiz, Assignment,AssignmentSubmission,QuizSubmission
from userauth.models import Teacher, Student

def get_current_academic_year():
    now = timezone.now()
    current_month = now.month

    if current_month in [8, 9, 10, 11, 12, 1]:  # Fall semester
        current_semester = 'Fall'
        if current_month == 1:  # January
            current_year = now.year - 1
        else:
            current_year = now.year
    elif current_month in [2, 3, 4, 5, 6, 7]:  # Winter semester
        current_semester = 'Winter'
        current_year = now.year - 1
    else:
        
        return None

    academic_year_name = f"{current_year}-{current_year + 1}"

    try:
        academic_year = AcademicYear.objects.get(academic_year_name=academic_year_name, academic_Semester=current_semester)
        return academic_year
    except AcademicYear.DoesNotExist:
       
        return None
    

def assessment_context_processor(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        current_academic_year_and_semester = get_current_academic_year()
        try:
            if user.role.role_name == "Student":
                student_profile = Student.objects.get(user=request.user)
                context['user_profile'] = user
                context['profile'] = student_profile
                current_semester = student_profile.semester
                current_enrollments = Enrollment.objects.filter(student=student_profile, course_semester__semester_year=current_semester)

                assignments = Assignment.objects.filter(teacher_course__course_semester__course__in=[enrollment.course_semester.course for enrollment in current_enrollments])
                quizzes = Quiz.objects.filter(teacher_course__course_semester__course__in=[enrollment.course_semester.course for enrollment in current_enrollments])
                
                submitted_assignments = AssignmentSubmission.objects.filter(student=student_profile, assignment__in=assignments)
                submitted_quizzes = QuizSubmission.objects.filter(student=student_profile, quiz__in=quizzes)
                
                submitted_assignment_ids = submitted_assignments.values_list('assignment_id', flat=True)
                submitted_quiz_ids = submitted_quizzes.values_list('quiz_id', flat=True)

                now = timezone.now()
                unsubmitted_assignments = assignments.filter(due_date__lt=now).exclude(assignment_id__in=submitted_assignment_ids)
                unsubmitted_quizzes = quizzes.filter(quiz_starting_date_and_time__lt=now).exclude(quiz_id__in=submitted_quiz_ids)
                
                pending_assignments = assignments.exclude(assignment_id__in=submitted_assignment_ids).exclude(due_date__lt=now)
                pending_quizzes = quizzes.exclude(quiz_id__in=submitted_quiz_ids).exclude(quiz_starting_date_and_time__lt=now)
                
                current_courses = [enrollment.course_semester.course for enrollment in current_enrollments]
                
                context['current_courses'] = current_courses
                context['current_enrollments'] = current_enrollments
                context['assignments'] = pending_assignments
                context['quizzes'] = pending_quizzes
                context['submitted_assignments'] = submitted_assignments
                context['submitted_quizzes'] = submitted_quizzes
                context['unsubmitted_assignments'] = unsubmitted_assignments
                context['unsubmitted_quizzes'] = unsubmitted_quizzes


            # For teachers
            elif user.role.role_name == "Teacher":
                context['user_profile'] = user
                teacher_profile = Teacher.objects.get(user=request.user)
                context['profile'] = teacher_profile
                teacher_courses = TeacherCourse.objects.filter(
                    teacher=teacher_profile,
                    course_semester__semester_year__academic_year=current_academic_year_and_semester
                )
                assignments = Assignment.objects.filter(teacher_course__in=teacher_courses)
                quizzes = Quiz.objects.filter(teacher_course__in=teacher_courses)
                context['teacher_courses'] = teacher_courses
                context['assignments'] = assignments
                context['quizzes'] = quizzes
                context['current_academic_year_and_semester'] = current_academic_year_and_semester
                
        except Exception as e:
            print(f"Error in context processor: {e}")
            pass


    return context



# def assessment_context_processor(request):
#     context = {}
#     if request.user.is_authenticated:
#         user = request.user
#         current_academic_year_and_semester = get_current_academic_year()
#         try:
#             if user.role.role_name == "Student":
#                 student_profile = Student.objects.get(user=request.user)
#                 context['user_profile'] = user
#                 context['profile'] = student_profile
#                 current_semester = student_profile.semester
#                 current_enrollments = Enrollment.objects.filter(
#                     student=student_profile,
#                     course_semester__semester_year=current_semester
#                 )

#                 assignments = Assignment.objects.filter(
#                     teacher_course__course_semester__course__in=[enrollment.course_semester.course for enrollment in current_enrollments]
#                 )
#                 quizzes = Quiz.objects.filter(
#                     teacher_course__course_semester__course__in=[enrollment.course_semester.course for enrollment in current_enrollments]
#                 )

#                 submitted_assignments = AssignmentSubmission.objects.filter(
#                     student=student_profile,
#                     assignment__in=assignments
#                 )
#                 submitted_quizzes = QuizSubmission.objects.filter(
#                     student=student_profile,
#                     quiz__in=quizzes
#                 )

#                 submitted_assignment_ids = submitted_assignments.values_list('assignment_id', flat=True)
#                 submitted_quiz_ids = submitted_quizzes.values_list('quiz_id', flat=True)

#                 now = timezone.now()
#                 unsubmitted_assignments = assignments.filter(due_date__lt=now).exclude(assignment_id__in=submitted_assignment_ids)
#                 unsubmitted_quizzes = quizzes.filter(due_date__lt=now).exclude(quiz_id__in=submitted_quiz_ids)

#                 pending_assignments = assignments.exclude(assignment_id__in=submitted_assignment_ids).exclude(due_date__lt=now)
#                 pending_quizzes = quizzes.exclude(quiz_id__in=submitted_quiz_ids).exclude(due_date__lt=now)

#                 current_courses = [enrollment.course_semester.course for enrollment in current_enrollments]

#                 context['current_courses'] = current_courses
#                 context['current_enrollments'] = current_enrollments
#                 context['assignments'] = pending_assignments
#                 context['quizzes'] = pending_quizzes
#                 context['submitted_assignments'] = submitted_assignments
#                 context['submitted_quizzes'] = submitted_quizzes
#                 context['unsubmitted_assignments'] = unsubmitted_assignments
#                 context['unsubmitted_quizzes'] = unsubmitted_quizzes
#         except Exception as e:
#             # Handle exception or log error
#             pass

#     return context