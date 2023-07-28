from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.exams, name='exams'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('<int:id>/', views.exam_details, name='exam_details'),
    path('get_classes/<int:id>/', views.get_classes, name='get_classes'),
    path('class_invitation/<int:id>/', views.class_invitation, name='class_invitation'),
    path('delete_course/<int:exam_id>/<int:course_id>/', views.delete_course, name='delete_course'),
    path('update/<int:id>/', views.update, name='update'),
    path('t_question_delete/<int:e_id>/<int:t_id>/', views.question_delete, name='t_question_delete'),
    path('d_question_delete/<int:e_id>/<int:d_id>/', views.question_delete, name='d_question_delete'),
    path('add_t_question/<int:id>/', views.add_t_question, name='add_t_question'),
    path('add_d_question/<int:id>/', views.add_d_question, name='add_d_question'),
    path('t_question/<int:e_id>/<int:t_id>/', views.t_question, name='t_question'),
    path('d_question/<int:e_id>/<int:t_id>/', views.d_question, name='d_question'),
    path('t_question/delete_img/<int:e_id>/<int:t_id>', views.t_question_delete_img, name='t_question_delete_img'),
    path('delete_choice/<int:id>/', views.delete_choice, name='delete_choice'),
    path('add_choice/<int:e_id>/<int:q_id>/', views.add_choice, name='add_choice'),
    path('t_question_update/<int:e_id>/<int:t_id>/', views.t_question_update, name='t_question_update'),
    path('d_question/delete_img/<int:e_id>/<int:d_id>', views.d_question_delete_img, name='d_question_delete_img'),
    path('d_question_update/<int:e_id>/<int:d_id>/', views.d_question_update, name='d_question_update'),
    path('enable_exam/<int:id>/', views.enable_exam, name='enable_exam'),
    path('close_exam/<int:id>/', views.close_exam, name='close_exam'),
    path('participate/<int:id>/', views.exam_participate, name='views.exam_participate'),
    path('analysis/<int:id>/',views.exam_analysis,name='exam_analysis'),
    path('analysis/<int:e_id>/<int:s_id>/',views.student_analysis,name='student_analysis')
]
