from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import *
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from django.contrib import messages
from django.http import HttpResponseNotFound
from exam.models import GrowthChart


def owner_required(login_url='portal:owner_login'):
    return user_passes_test(lambda u: u.role == 'Owner', login_url=login_url)


@login_required(login_url='accounts:login')
@owner_required()
def students(request):
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    student = academy.students.all().order_by('-create')
    context = {'student': student, 'academy': academy}
    return render(request, 'users/students.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def student_details(request, id):
    student = get_object_or_404(User, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if not student in academy.students.all():
        return HttpResponseNotFound
    chart = GrowthChart.objects.filter(student=student)
    context = {'student': student,'chart':chart}
    return render(request, 'users/student_details.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def student_add(request):
    url = request.META.get('HTTP_REFERER')
    form1 = FLProfileForm(request.POST)
    form2 = StudentCodeForm(request.POST)
    if form1.is_valid() and form2.is_valid():
        data1 = form1.cleaned_data
        data2 = form2.cleaned_data['national_code']
        students = Academy.objects.get(id=request.user.owner_profile.academy.id).students
        if students.filter(national_code=data2).exists():
            messages.warning(request, 'کد ملی موجود میباشد')
            return redirect(url)
        student = User.objects.create_user(national_code=data2, password=str(data2), email=None, phone=None)
        student.email_phone = data2
        student.is_active = True
        student.role = 'Student'
        student.save()
        StudentProfile.objects.create(student=student, first_name=data1['first_name'], last_name=data1['last_name'])
        students.add(student)
        messages.success(request, 'با موفقیت اضافه شد')
    else:
        messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def student_delete(request, id):
    student = get_object_or_404(User, id=id)
    academy_students = Academy.objects.get(id=request.user.owner_profile.academy.id).students.all()
    if student in academy_students:
        student.delete()
        messages.success(request, 'با موفقیت حذف شد')
    else:
        return HttpResponseNotFound()
    return redirect('users:students')


@login_required(login_url='accounts:login')
@owner_required()
def student_update(request, id):
    url = request.META.get('HTTP_REFERER')
    student = get_object_or_404(User, id=id)
    academy_students = Academy.objects.get(id=request.user.owner_profile.academy.id).students.all()
    if student in academy_students:
        if request.method == 'POST':
            form1 = FLProfileForm(request.POST, instance=student.student_profile)
            form2 = StudentCodeForm(request.POST, instance=student)
            if form1.is_valid() and form2.is_valid():
                data1 = form1.cleaned_data
                data2 = form2.cleaned_data
                form1.save()
                form2.save()
                messages.success(request, 'با موفقیت ذخیره شد')
            else:
                messages.error(request, 'لطفا مقدار معتبر وارد کنید')
    else:
        return HttpResponseNotFound()
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def student_reset(request, id):
    url = request.META.get('HTTP_REFERER')
    student = get_object_or_404(User, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if not student in academy.students.all():
        return HttpResponseNotFound
    student.set_password(str(student.national_code))
    messages.success(request, 'رمز با موفقیت بازنشانی شد')
    context = {'student': student}
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def teachers(request):
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    teacher = academy.teachers.all().order_by('-create')
    context = {'teacher': teacher, 'academy': academy}
    return render(request, 'users/teachers.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def teacher_details(request, id):
    teacher = get_object_or_404(User, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if not teacher in academy.teachers.all():
        return HttpResponseNotFound
    courses = academy.courses.all()
    context = {'teacher': teacher,'courses':courses}
    return render(request, 'users/teacher_details.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def teacher_add(request):
    url = request.META.get('HTTP_REFERER')
    form1 = FLProfileForm(request.POST)
    form2 = TeacherCodeForm(request.POST)
    if form1.is_valid() and form2.is_valid():
        data1 = form1.cleaned_data
        data2 = form2.cleaned_data
        teachers = Academy.objects.get(id=request.user.owner_profile.academy.id).teachers
        if teachers.filter(national_code=data2['national_code']).exists():
            messages.warning(request, 'کد ملی موجود میباشد')
            return redirect(url)
        if teachers.filter(phone=data2['phone']).exists():
            messages.warning(request, 'شماره موبایل موجود میباشد')
            return redirect(url)
        teacher = User.objects.create_user(national_code=data2['national_code'],
                                           phone=data2['phone'], email='test@gmail.com',
                                           password=str(data2['phone']))
        teacher.email_phone = data2['national_code']
        teacher.role = 'Teacher'
        teacher.is_active = True
        teacher.email = None
        teacher.save()
        TeacherProfile.objects.create(teacher=teacher, first_name=data1['first_name'], last_name=data1['last_name'])
        teachers.add(teacher)
        teacher.save()
        messages.success(request, 'با موفقیت اضافه شد')
    else:
        messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def teacher_delete(request, id):
    teacher = get_object_or_404(User, id=id)
    academy_teachers = Academy.objects.get(id=request.user.owner_profile.academy.id).teachers.all()
    if teacher in academy_teachers:
        teacher.delete()
        messages.success(request, 'با موفقیت حذف شد')
    else:
        return HttpResponseNotFound()
    return redirect('users:teachers')


@login_required(login_url='accounts:login')
@owner_required()
def teacher_update(request, id):
    url = request.META.get('HTTP_REFERER')
    teacher = get_object_or_404(User, id=id)
    academy_teachers = Academy.objects.get(id=request.user.owner_profile.academy.id).teachers.all()
    if teacher in academy_teachers:
        if request.method == 'POST':
            form1 = FLProfileForm(request.POST, instance=teacher.teacher_profile)
            form2 = TeacherCodeForm(request.POST, instance=teacher)
            if form1.is_valid() and form2.is_valid():
                data1 = form1.cleaned_data
                data2 = form2.cleaned_data
                form1.save()
                form2.save()
                messages.success(request, 'با موفقیت ذخیره شد')
            else:
                messages.error(request, 'لطفا مقدار معتبر وارد کنید')
    else:
        return HttpResponseNotFound()
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def teacher_reset(request, id):
    url = request.META.get('HTTP_REFERER')
    teacher = get_object_or_404(User, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if not teacher in academy.teachers.all():
        return HttpResponseNotFound
    teacher.set_password(str(teacher.national_code))
    messages.success(request, 'رمز با موفقیت بازنشانی شد')
    return redirect(url)
