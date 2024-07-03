from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Assignment, AssignmentSubmission, Quiz, QuizSubmission, QuizQuestion, QuizAnswer
from .forms import AssignmentCreateForm, AssignmentSubmissionForm, QuizCreateForm, QuizQuestionForm
from academics.models import TeacherCourse,Enrollment,Course
from .forms import QuizCreateForm, QuizQuestionForm
from django.forms import modelformset_factory
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.utils.timezone import localtime
from userauth.models import Student
# from assessment.context_processor import get_current_academic_year
import datetime

@login_required
def open_Assignment(request,course_id):
    course=get_object_or_404(Course,course_id=course_id)
    context={}
    context['course']=course
    return render(request,"assessment/assignment/assignment_view.html",context)

@login_required
def create_assignment(request, teacher_course_id):
    teacher_course = get_object_or_404(TeacherCourse, teacher_course_id=teacher_course_id, teacher=request.user.teacher)

    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher_course = teacher_course
            assignment.save()
            return redirect('assignments_list')  # Replace with your actual redirect URL
    else:
        form = AssignmentCreateForm()

    context = {
        'form': form,
        'teacher_course': teacher_course,
    }
    return render(request, 'assessment/assignment/create_assignment.html', context)



@login_required
def edit_assignment(request,teacher_course_id,assignment_id):
    teacher_course = get_object_or_404(TeacherCourse, teacher_course_id=teacher_course_id, teacher=request.user.teacher)
    assignment=get_object_or_404(Assignment,assignment_id=assignment_id)


    if request.method=='POST':
        form =AssignmentCreateForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            redirect('assessment:assignment-list', teacher_course_id = teacher_course.teacher_course_id)
    else:
            form =AssignmentCreateForm(instance= assignment)
    context ={
            'form':form,
            'teacher_course':teacher_course
        }
    return render(request,'assessment/assignment/edit_assignment.html',context)

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id)
    student = request.user.student  # assuming the user is linked to a student profile
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = student
            submission.assignment = assignment
            submission.save()
            # return redirect('assignment_detail', assignment_id=assignment_id)  # Update this with your actual redirect URL
    else:
        form = AssignmentSubmissionForm()
    
    return render(request, 'assessment/assignment/submit_assignment.html', {'form': form, 'assignment': assignment})


@login_required
def teacher_view_of_assignments(request, teacher_course_id):
    # Get the TeacherCourse object using the teacher_course_id
    teacher_course = get_object_or_404(TeacherCourse, teacher_course_id=teacher_course_id)

    # Ensure the logged-in teacher is the one associated with the teacher_course
    if request.user.teacher != teacher_course.teacher:
        return redirect('some_error_page')  # Replace with appropriate error handling

    # Get all assignments created by the teacher for this course
    assignments = Assignment.objects.filter(teacher_course=teacher_course)
    
    # Create a list to hold assignments and their respective submissions
    assignments_with_submissions = []
    for assignment in assignments:
        submissions = AssignmentSubmission.objects.filter(assignment=assignment)
        assignments_with_submissions.append({
            'assignment': assignment,
            'submissions': submissions
        })

    context = {
        'assignments_with_submissions': assignments_with_submissions,
        'teacher_course': teacher_course,
    }
    
    return render(request, 'assessment/assignment/teacher_assignments.html', context)

