from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('<slug>/', views.academy_page, name='academy_page'),
    path('login/<int:id>/', views.teacher_login, name='teacher_login'),
    path('<slug>/dashboard/', views.dashboard, name='dashboard'),
    path('<slug>/profile/', views.profile, name='profile'),
    path('<slug>/courses/', views.courses, name='courses'),
    path('<slug>/logout/', views.t_logout, name='logout'),
    path('<slug>/exams/', views.exams, name='exams'),
    path('<slug>/analysis/<int:id>/', views.exam_analysis, name='exam_analysis'),
    path('t_analysis/<int:e_id>/<int:s_id>/',views.student_analysis,name='student_analysis')
]
