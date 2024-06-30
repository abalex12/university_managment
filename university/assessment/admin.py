from django.contrib import admin
from .models import Assignment, AssignmentSubmission, Quiz, QuizQuestion, QuizSubmission, QuizAnswer

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher_course', 'due_date', 'max_score']
    search_fields = ['title', 'teacher_course__course__course_name']

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'score']
    search_fields = ['assignment__title', 'student__user__username']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher_course', 'quiz_starting_date_and_time', 'total_questions', 'max_score']
    search_fields = ['title', 'teacher_course__course__course_name']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text']
    search_fields = ['quiz__title', 'question_text']

@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'student', 'submitted_at', 'score']
    search_fields = ['quiz__title', 'student__user__username']

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['submission', 'question', 'selected_choice']
    search_fields = ['submission__quiz__title', 'question__question_text', 'choice__choice_text']
