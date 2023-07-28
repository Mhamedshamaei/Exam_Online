from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import *
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.http import JsonResponse


def owner_required(login_url='portal:owner_login'):
    return user_passes_test(lambda u: u.role == 'Owner', login_url=login_url)


@login_required(login_url='accounts:login')
@owner_required()
def courses(request):
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    courses = academy.courses.all().order_by('-create')
    context = {'courses': courses}
    return render(request, 'courses/courses.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def add(request):
    url = request.META.get('HTTP_REFERER')
    form = CoursesCreateForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data['name']
        course = Courses.objects.create(name=data, )
        Academy.objects.get(id=request.user.owner_profile.academy.id).courses.add(course)
        messages.success(request, 'با موفقیت اضافه شد')
    else:
        messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def delete(request, id):
    url = request.META.get('HTTP_REFERER')
    course = get_object_or_404(Courses, id=id)
    academy_courses = Academy.objects.get(id=request.user.owner_profile.academy.id).courses.all()
    if course in academy_courses:
        course.delete()
        messages.success(request, 'با موفقیت حذف شد')
    else:
        return HttpResponseNotFound()
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def update(request, id):
    url = request.META.get('HTTP_REFERER')
    course = get_object_or_404(Courses, id=id)
    if request.method == 'POST':
        form = CoursesCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['name']
            academy_courses = Academy.objects.get(id=request.user.owner_profile.academy.id).courses.all()
            if course in academy_courses:
                course.name = data
                course.save()
                messages.success(request, 'با موفقیت ویرایش شد')
            else:
                return HttpResponseNotFound()
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def details(request, id):
    course = get_object_or_404(Courses, id=id)
    if not course in Academy.objects.get(id=request.user.owner_profile.academy.id).courses.all():
        return HttpResponseNotFound()
    students = course.students.all().order_by('-create')
    teachers = course.teachers.all().order_by('-create')
    context = {'course': course, 'students': students, 'teachers': teachers}
    return render(request, 'courses/details.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def get_teachers(request, id):
    course = get_object_or_404(Courses, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if not course in academy.courses.all():
        return HttpResponseNotFound()
    context = {}
    for t in academy.teachers.all():
        if t not in course.teachers.all():
            context[t.id] = f'{t.teacher_profile.first_name} {t.teacher_profile.last_name}'
    return JsonResponse(context)


@login_required(login_url='accounts:login')
@owner_required()
def get_students(request, id):
    course = get_object_or_404(Courses, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if not course in academy.courses.all():
        return HttpResponseNotFound()
    context = {}
    for s in academy.students.all():
        if s not in course.students.all():
            context[s.id] = f'{s.student_profile.first_name} {s.student_profile.last_name}'
    return JsonResponse(context)


@login_required(login_url='accounts:login')
@owner_required()
def teacher_invitation(request, id):
    course = get_object_or_404(Courses, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if not course in academy.courses.all():
        return HttpResponseNotFound()
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AddJsDic(request.POST)
        if form.is_valid():
            data = form.cleaned_data['dic'].split(',')
            for i in data:
                if i:
                    teacher = User.objects.filter(id=int(i))
                    if teacher.exists():
                        course.teachers.add(User.objects.get(id=int(i.replace(',', ''))).id)
                        course.save()
                        messages.success(request, 'با موفقیت دعوت شد')
                    else:
                        messages.error(request, 'لطفا مقدار صحیح وارد کنید')
                        return redirect(url)
        else:
            messages.warning(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def student_invitation(request, id):
    course = get_object_or_404(Courses, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if not course in academy.courses.all():
        return HttpResponseNotFound()
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AddJsDic(request.POST)
        if form.is_valid():
            data = form.cleaned_data['dic'].split(',')
            for i in data:
                if i:
                    student = User.objects.filter(id=int(i))
                    if student.exists():
                        course.students.add(User.objects.get(id=int(i.replace(',', ''))).id)
                        course.save()
                        for s in student:
                            s.student_profile.now_courses.add(course)
                        messages.success(request, 'با موفقیت دعوت شد')
                    else:
                        messages.error(request, 'لطفا مقدار صحیح وارد کنید')
                        return redirect(url)
        else:
            messages.warning(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def user_delete(request, course_id, teacher_id=None, student_id=None):
    url = request.META.get('HTTP_REFERER')
    course = get_object_or_404(Courses, id=course_id)
    academy_courses = Academy.objects.get(id=request.user.owner_profile.academy.id).courses.all()
    if course in academy_courses:
        if teacher_id:
            teacher = course.teachers.filter(id=teacher_id)
            if teacher.exists():
                id = course.teachers.get(id=teacher_id).id
                course.teachers.remove(id)
                messages.success(request, 'حذف شد')
            else:
                return HttpResponseNotFound()
        else:
            student = course.students.filter(id=student_id)
            if student.exists():
                id = course.students.get(id=student_id).id
                course.students.remove(id)
                for s in student:
                    s.student_profile.now_courses.remove(course)
                messages.success(request, 'حذف شد')
            else:
                return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()
    return redirect(url)
