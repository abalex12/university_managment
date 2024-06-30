from django.urls import path
from .views import *
from django.views.generic import TemplateView

app_name="academics"

urlpatterns=[
    path('detail/',display_detail,name="detail"),
    path('course-registration/', course_registration, name='course_registration'),   
    path('edit-detail/',edit_profile,name="edit_detail"),
    # path('teacher/courses/', teacher_courses_view, name='teacher_courses'),

]