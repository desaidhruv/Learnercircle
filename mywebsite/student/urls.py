from django.urls import path
from . import views
from .views import ActivateAccountView
from django.contrib.auth import views as auth_views

app_name = 'student'
urlpatterns = [
    path('', views.index, name= "index"),
    path('dashboard/', views.dashboard, name= "dashboard"),
    path('mycourses/', views.mycourses, name= "mycourses"),
    path('courses/', views.courses, name= "courses"),
    path('competitions/', views.competitions, name= "competitions"),
    path('showcase/', views.showcase, name= "showcase"),
    path('courseDetails/<pk>/', views.CourseDetailView.as_view(), name= "courseDetails"),
    path('competitionDetail/<pk>/', views.CompetitionDetailView.as_view(), name= "competitionDetails"),
    path('category/<category>/',views.CategoryView.as_view(),name='course_category'),
    path('register/', views.register_page, name= "register"),

    path('check_user/', views.check_user, name= "check_user"),
    path('check_email/', views.check_email, name= "check_email"),
    
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
]