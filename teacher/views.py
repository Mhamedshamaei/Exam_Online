from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound
from exam.models import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='accounts:login')
def academy_page(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    images = AcademyGallery.objects.filter(academy=academy)
    context = {'academy': academy, 'images': images}
    return render(request, 'teacher/login.html', context)


@login_required(login_url='accounts:login')
def teacher_login(request, id):
    academy = get_object_or_404(Academy, id=id)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, email_phone=data['email_phone'], password=data['password'])
            if user in academy.teachers.all():
                login(request, user)
                user.teacher_profile.now_academy = academy
                user.teacher_profile.save()
                messages.success(request, 'با موفقیت وارد شدید')
                return redirect('teacher:dashboard', academy.url)
            else:
                messages.error(request, 'کاربری با این مشخصات وجود ندارد')
        else:
            messages.error(request, 'لطفا مقدار معتبر وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
def dashboard(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.teachers.all():
        return HttpResponseNotFound()
    return render(request, 'teacher/dashboard.html')


@login_required(login_url='accounts:login')
def profile(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.teachers.all():
        return HttpResponseNotFound()
    teacher = get_object_or_404(User, id=request.user.id)
    context = {'teacher': teacher}
    return render(request, 'teacher/profile.html', context)


@login_required(login_url='accounts:login')
def courses(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.teachers.all():
        return HttpResponseNotFound()
    courses = academy.courses.filter(teachers=request.user)
    context = {'courses': courses}
    return render(request, 'teacher/courses.html', context)


@login_required(login_url='accounts:login')
def t_logout(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.teachers.all():
        return HttpResponseNotFound()
    request.user.teacher_profile.now_academy = None
    request.user.teacher_profile.save()
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('teacher:academy_page', academy.url)


@login_required(login_url='accounts:login')
def exams(request, slug):
    academy = get_object_or_404(Academy, url=slug)
    if not request.user in academy.teachers.all():
        return HttpResponseNotFound()
    exam = Exam.objects.filter(academy=academy)
    context = {'exams': exam, }
    return render(request, 'teacher/exams.html', context)


@login_required(login_url='accounts:login')
def exam_analysis(request, slug, id):
    academy = get_object_or_404(Academy, url=slug)
    exam = get_object_or_404(Exam, id=id)
    if not request.user in exam.access_teachers.all() or not exam.closed:
        return HttpResponseNotFound()
    sheets = AnswerSheet.objects.filter(exam=exam)
    true = 0
    false = 0
    total = 0
    for i in sheets:
        true += i.get_true()
        false += i.get_false()
        total += i.get_total()
    l_true = int(true / sheets.count())
    l_false = int(false / sheets.count())
    l_total = int(total / sheets.count())
    students = exam.student_dones.all()
    context = {'exam': exam, 'l_true': l_true, 'l_false': l_false, 'l_total': l_total, 'students': students}
    return render(request, 'teacher/analysis.html', context)


@login_required(login_url='accounts:login')
def student_analysis(request, e_id, s_id):
    exam = get_object_or_404(Exam, id=e_id)
    student = get_object_or_404(User, id=s_id)
    if request.user not in exam.access_teachers.all():
        return HttpResponseNotFound()
    sheet = get_object_or_404(AnswerSheet, student=student, exam=exam)
    chart = GrowthChart.objects.filter(student=student)
    context = {'sheet': sheet, 'exam': exam, 'chart': chart, 'student': student}
    return render(request, 'exam/student_analysis.html', context)
