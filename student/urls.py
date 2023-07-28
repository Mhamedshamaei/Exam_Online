from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('<slug>/', views.academy_page, name='academy_page'),
    path('login/<int:id>/', views.student_login, name='student_login'),
    path('<slug>/dashboard/', views.dashboard, name='dashboard'),
    path('<slug>/profile/', views.profile, name='profile'),
    path('<slug>/courses/', views.courses, name='courses'),
    path('<slug>/logout/', views.s_logout, name='logout'),
    path('<slug>/n_exam/', views.n_exam, name='n_exam'),
    path('<slug>/l_exam/', views.l_exam, name='l_exam'),
    path('<slug>/exam/<int:id>/', views.exam_details, name='exam_details'),
]
