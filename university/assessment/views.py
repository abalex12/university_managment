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
from assessment.context_processor import get_current_academic_year

import datetime




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
def open_sections(reqeust):
    return render(reqeust,'academics/teacher_sections.html')
@login_required
def open_Assignment(request,course_id):
    course=get_object_or_404(Course,course_id=course_id)
    context={}
    context['course']=course
    return render(request,"assessment/assignment/assignment_view.html",context)
@login_required
def open_Quiz(request,course_id):
    course=get_object_or_404(Course,course_id=course_id)
    return render(request,"assessment/quiz/Quiz_view.html",{"course":course})

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

@login_required
def create_quiz(request, teacher_course_id):
    teacher_course = get_object_or_404(TeacherCourse, teacher_course_id=teacher_course_id)
    if request.method == 'POST':
        form = QuizCreateForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.teacher_course = teacher_course
            quiz.save()
            return redirect('assessment:add_questions', quiz_id=quiz.quiz_id)
    else:
        form = QuizCreateForm()
    return render(request, 'assessment/quiz/create_quiz.html', {'form': form, 'teacher_course': teacher_course})

@login_required
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    QuizQuestionFormSet = modelformset_factory(QuizQuestion, form=QuizQuestionForm, extra=quiz.total_questions) 
    if request.method == 'POST':
        formset = QuizQuestionFormSet(request.POST, request.FILES, queryset=QuizQuestion.objects.none())
        if formset.is_valid():
            for form in formset:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()
            return redirect('assessment:quiz_detail', quiz_id=quiz.quiz_id)
    else:
        formset = QuizQuestionFormSet(queryset=QuizQuestion.objects.none())
    return render(request, 'assessment/quiz/add_questions.html', {'formset': formset, 'quiz': quiz})


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = QuizQuestion.objects.filter(quiz=quiz)
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'assessment/quiz/quiz_detail.html', context)




@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    questions = quiz.questions.all()
    interval = quiz.time_limit
    time_limit = datetime.timedelta(minutes=interval)
    student = get_object_or_404(Student, user=request.user)

    submission = QuizSubmission.objects.filter(quiz=quiz, student=student).first()
    if submission:
        return HttpResponseForbidden("You have already submitted this quiz.")

    current_datetime = localtime(timezone.now())
    start_datetime = localtime(quiz.quiz_starting_date_and_time)

    if current_datetime < start_datetime:
        remaining_time = (start_datetime - current_datetime).total_seconds()
        return render(request, 'academics/quiz/quiz_countdown.html', {
            'quiz': quiz,
            'remaining_time': remaining_time,
        })

    if 'start_time' not in request.session:
        request.session['start_time'] = timezone.now().isoformat()

    start_time = timezone.datetime.fromisoformat(request.session['start_time'])
    elapsed_time = (timezone.now() - start_time).total_seconds()

    if elapsed_time > time_limit.total_seconds():
        return HttpResponseForbidden("Time is up!")

    if request.method == 'POST':
        submission = QuizSubmission.objects.create(
            quiz=quiz,
            student=student,
            submitted_at=timezone.now(),
            score=0
        )
        for question in questions:
            selected_choice = request.POST.get(f'question_{question.question_id}')
            if selected_choice:
                QuizAnswer.objects.create(
                    submission=submission,
                    question=question,
                    selected_choice=selected_choice
                )
        submission.save()
        return redirect('assessment:quiz_results', quiz_id=quiz_id)

    context = {
        'quiz': quiz,
        'questions': questions,
        'time_limit': time_limit.total_seconds() - elapsed_time,
    }
    return render(request, 'assessment/quiz/take_quiz.html', context)


@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    submission = get_object_or_404(QuizSubmission, quiz=quiz, student=request.user)
    answers = QuizAnswer.objects.filter(submission=submission)

    context = {
        'quiz': quiz,
        'submission': submission,
        'answers': answers,
    }
    return render(request, 'academics/quiz/quiz_results.html', context)
