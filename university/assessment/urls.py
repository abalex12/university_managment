from django.urls import path
from .views import *

app_name='assessment'

urlpatterns =[
    path('section/',open_sections,name="sections"),
    path('create-assignment/<str:teacher_course_id>',create_assignment,name="create_assignment"),
    # path('student-assignments/ <str:course_id>', course_assignments, name='course_assignments'),
    path('submit-assignment/<str:assignment_id>',submit_assignment , name='submit_assignment'),
    path('teacher-assignment/<str:teacher_course_id>', teacher_view_of_assignments,name='teacher_assignments'),
    path('assignment/<str:course_id>',open_Assignment,name="assignment_view"),
    path('quiz/<str:course_id>',open_Quiz, name="Quiz_view"),
    path('create-quiz/<str:teacher_course_id>/', create_quiz, name='create_quiz'),
    path('add-questions/<str:quiz_id>/', add_questions, name='add_questions'),
    path('take-quiz/<str:quiz_id>/', take_quiz, name='take_quiz'),
    path('quiz-detail/<str:quiz_id>/', quiz_detail, name='quiz_detail'),
    path("edit-assignment/<str:teacher_course_id>/<str:assignment_id>",edit_assignment,name='edit-assignment'),
]