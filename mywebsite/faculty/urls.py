from django.contrib import admin
from django.urls import path
from . import views
from .views import ActivateAccountView
from django.contrib.auth import views as auth_views

app_name = 'faculty'
urlpatterns = [
    path('', views.index, name= "index"),
    # path('form_submit/', views.form_submit, name= "form_submit"),
    #Authentication
    path('register/', views.register_page, name= "register"),

    path('check_user/', views.check_user, name= "check_user"),
    path('check_email/', views.check_email, name= "check_email"),
    
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
    
    
    #Faculty Pages
    path('profile_section/', views.profile_section, name= "profile_section"),
    path('profile_section_submit/', views.profile_section_submit, name= "profile_section_submit"),
    path('course_section/', views.course_section, name= "course_section"),
    path('course_section_submit/', views.course_section_submit, name= "course_section_submit"),
    path('course_new/', views.course_new, name= "course_new"),
    path('bank_details/', views.bank_details, name= "bank_details"),
    path('bank_details_submit/', views.bank_details_submit, name= "bank_details_submit"),
    path('course_overview/', views.course_overview, name= "course_overview"),
    path('course_overview_submit/', views.course_overview_submit, name= "course_overview_submit"),
    path('schedule/', views.schedule, name= "schedule"),
    path('schedule_submit/', views.schedule_submit, name= "schedule_submit"),
    path('feedback/', views.feedback, name= "feedback"),
    path('dashboard/', views.dashboard, name= "dashboard"),

]