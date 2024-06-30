from django.urls import path
from .views import *



app_name = "userauth"

urlpatterns =[
    path('',index,name="index"),
    path('sign-out/', logout_view, name="sign-out"),
    path('dashboard/', log_in, name="dashboard"),
    path('sign-in/', signin, name="sign-in"),
    path('sign-up/', signup, name="sign-up"),
]