from django.urls import path
from . import views

app_name = 'participate'

urlpatterns = [
    path('exam/<int:id>/',views.load_exam,name='load_exam'),
    path('send/<int:id>/',views.send,name='send'),
]
