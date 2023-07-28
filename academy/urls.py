from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('',views.academy,name='academy'),
    path('add_img/',views.add_img,name='add_img'),
    path('delete_img/<int:id>/',views.delete_img,name='delete_img')
]
