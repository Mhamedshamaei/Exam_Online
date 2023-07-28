from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('students/',views.students,name='students'),
    path('student/<int:id>/',views.student_details,name='student_details'),
    path('student_add/',views.student_add,name='student_add'),
    path('student_delete/<int:id>/',views.student_delete,name='student_delete'),
    path('student_update/<int:id>/',views.student_update,name='student_update'),
    path('student_reset/<int:id>/',views.student_reset,name='student_reset'),
    path('teachers/',views.teachers,name='teachers'),
    path('teacher/<int:id>/',views.teacher_details,name='teacher_details'),
    path('teacher_add/',views.teacher_add,name='teacher_add'),
    path('teacher_delete/<int:id>/',views.teacher_delete,name='teacher_delete'),
    path('teacher_update/<int:id>/',views.teacher_update,name='teacher_update'),
    path('teacher_reset/<int:id>/',views.teacher_reset,name='teacher_reset')
]
