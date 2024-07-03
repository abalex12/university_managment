from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, QuizSubmission, QuizQuestion, QuizAnswer
from .forms import  QuizCreateForm, QuizQuestionForm
from academics.models import TeacherCourse,Course
from django.forms import modelformset_factory
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.utils.timezone import localtime
from userauth.models import Student
# from assessment.context_processor import get_current_academic_year
import datetime
from django.contrib import messages



@login_required
def open_Quiz(request,course_id):
    course=get_object_or_404(Course,course_id=course_id)
    return render(request,"assessment/quiz/Quiz_view.html",{"course":course})



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
            print("hlp")
    else:
        formset = QuizQuestionFormSet(queryset=QuizQuestion.objects.none())
    return render(request, 'assessment/quiz/add_questions.html', {'formset': formset, 'quiz': quiz})
@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = QuizQuestion.objects.filter(quiz=quiz)
    QuizQuestionFormSet = modelformset_factory(QuizQuestion, form=QuizQuestionForm, extra=0)

    if request.method == 'POST':
        question_formset = QuizQuestionFormSet(request.POST,request.FILES, queryset=questions)
        if question_formset.is_valid():
           
            question_formset.save()
            return redirect('assessment:quiz_detail', quiz_id=quiz_id)
        
    else:
        question_formset = QuizQuestionFormSet(queryset=questions)

    context = {
        'quiz': quiz,
        'questions': questions,
        'question_formset': question_formset,
    }
    return render(request, 'assessment/quiz/quiz_detail.html', context)

@login_required
def quiz_list(request,teacher_course_id):
    teachercourse=get_object_or_404(TeacherCourse,teacher_course_id=teacher_course_id)
    context={
        'teachercourse':teachercourse
    }
    return render(request,'assessment/quiz/quiz-list.html',context)
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
        total_score = 0
        for question in questions:
            selected_choice = request.POST.get(f'question_{question.question_id}')
            if selected_choice:
                is_correct = int(selected_choice) == question.get_correct_choice()
                if is_correct:
                    total_score += 1
                QuizAnswer.objects.create(
                    submission=submission,
                    question=question,
                    selected_choice=selected_choice
                )
        submission.score = (total_score * quiz.max_score)/ quiz.total_questions
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
    submission = get_object_or_404(QuizSubmission, quiz=quiz, student=request.user.student)
    answers = QuizAnswer.objects.filter(submission=submission)
    
    # Calculate the correct answers
    questions_with_answers = []
    for answer in answers:
        question = answer.question
        correct_choice = question.get_correct_choice()
        
        questions_with_answers.append({
            'question': question,
            'answer': answer,
            'correct_choice': correct_choice
        })
    
    context = {
        'quiz': quiz,
        'submission': submission,
        'questions_with_answers': questions_with_answers,
    }
    return render(request, 'assessment/quiz/quiz_result.html', context)

@login_required
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, quiz_id=quiz_id)
    teachercourse_id = quiz.teacher_course.teacher_course_id  # Assuming the relationship exists
    print(teachercourse_id)
    if request.method == 'POST':
        quiz.delete()
        # print("jlsf")
        messages.success(request, 'Quiz deleted successfully.')  # Add success message
        return redirect('assessment:quiz_list', teacher_course_id=teachercourse_id)
    
    # Handle GET request with a confirmation form or direct deletion
    # This part can be adjusted based on your UI/UX flow for deletion
    
    return redirect('assessment:quiz_list', teacher_course_id=teachercourse_id)