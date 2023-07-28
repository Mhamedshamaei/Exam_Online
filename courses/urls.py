from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.courses, name='courses'),
    path('add/', views.add, name='add'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('update/<int:id>/', views.update, name='update'),
    path('<int:id>/', views.details, name='details'),
    path('get_teachers/<int:id>/', views.get_teachers, name='get_teachers'),
    path('get_students/<int:id>/', views.get_students, name='get_students'),
    path('teacher_invitation/<int:id>/', views.teacher_invitation, name='teacher_invitation'),
    path('student_invitation/<int:id>/', views.student_invitation, name='student_invitation'),
    path('teacher_delete/<int:course_id>/<int:teacher_id>/', views.user_delete, name='teacher_delete'),
    path('student_delete/<int:course_id>/<int:student_id>/', views.user_delete, name='student_delete'),
]
