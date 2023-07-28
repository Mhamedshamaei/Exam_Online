from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('resend/<uidb64>/<token>/', views.resend, name='resend'),
    path('active/<uidb64>/<token>/', views.active, name='active'),
    path('login/', views.u_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.u_logout, name='logout'),
]
