"""
URL configuration for ExamOnline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('academy/',include('academy.urls',namespace='academy')),
    path('courses/',include('courses.urls',namespace='courses')),
    path('users/',include('users.urls',namespace='users')),
    path('student/',include('student.urls',namespace='student')),
    path('teacher/',include('teacher.urls',namespace='teacher')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard')),
    path('exam/',include('exam.urls',namespace='exam')),
    path('plans/',include('plans.urls',namespace='plans')),
    path('participate/',include('participate.urls',namespace='participate'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
