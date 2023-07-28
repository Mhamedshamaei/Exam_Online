from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound
from exam.models import *
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse


def academy_page(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    images = AcademyGallery.objects.filter(academy=academy)
    context = {'academy': academy, 'images': images}
    return render(request, 'student/login.html', context)


def student_login(request, id):
    academy = get_object_or_404(Academy, id=id)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, email_phone=data['email_phone'], password=data['password'])
            if user in academy.students.all():
                login(request, user)
                user.student_profile.now_academy = academy
                user.student_profile.save()
                academy.students.add(user)
                messages.success(request, 'با موفقیت وارد شدید')
                return redirect('student:dashboard', academy.url)
            else:
                messages.error(request, 'کاربری با این مشخصات وجود ندارد')
        else:
            messages.error(request, 'لطفا مقدار معتبر وارد کنید')
    return redirect(url)


def dashboard(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.students.all():
        return HttpResponseNotFound()
    return render(request, 'student/dashboard.html')


def profile(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.students.all():
        return HttpResponseNotFound()
    student = get_object_or_404(User, id=request.user.id)
    context = {'student': student}
    return render(request, 'student/profile.html', context)


def courses(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.students.all():
        return HttpResponseNotFound()
    courses = request.user.student_profile.now_courses.all()
    context = {'courses': courses}
    return render(request, 'student/course.html', context)


def s_logout(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.students.all():
        return HttpResponseNotFound()
    request.user.student_profile.now_academy = None
    request.user.student_profile.save()
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('student:academy_page', academy.url)


def n_exam(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.students.all():
        return HttpResponseNotFound()
    exams = request.user.exam_s_access.filter(
        Q(end_date=None, active=True) | Q(end_date__lte=timezone.now().date(), active=True)).order_by('-create')
    can_start = request.user.exam_s_access.filter(start_date__lte=timezone.now().date(),
                                                  start_time__lte=timezone.now().time())
    context = {'exams': exams, 'can_start': can_start}
    return render(request, 'student/n_exam.html', context)


def l_exam(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.students.all():
        return HttpResponseNotFound()
    exams = request.user.exam_s_done.all().order_by('-create')
    context = {'exams': exams, }
    return render(request, 'student/l_exam.html', context)


def exam_details(request, slug, id):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.students.all():
        return HttpResponseNotFound()
    exam = get_object_or_404(Exam, id=id)
    if not request.user in exam.student_dones.all():
        return HttpResponseNotFound()
    sheet = get_object_or_404(AnswerSheet, student=request.user, exam=exam)
    chart = GrowthChart.objects.filter(student=request.user)
    context = {'sheet': sheet, 'exam': exam,'chart':chart}
    return render(request, 'student/exam_details.html', context)
