from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from accounts.models import *
from .models import *
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib import messages
from .forms import *
from django.http import JsonResponse
from courses.forms import AddJsDic
from itertools import chain


def owner_required(login_url='portal:owner_login'):
    return user_passes_test(lambda u: u.role == 'Owner', login_url=login_url)


@login_required(login_url='accounts:login')
@owner_required()
def exams(request):
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    exams = Exam.objects.filter(academy=academy).order_by('-create')
    context = {'exams': exams}
    return render(request, 'exam/exam.html', context)


@login_required(login_url='accounts:login')
def delete(request, id):
    exam = get_object_or_404(Exam, id=id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
        if exam.academy != academy:
            return HttpResponseNotFound()
        exam.delete()
        messages.success(request, 'با موفقیت حذف شد')
        return redirect('exam:exams')
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        if exam.academy != academy or request.user not in exam.access_teachers.all():
            return HttpResponseNotFound()
        exam.delete()
        messages.success(request, 'با موفقیت حذف شد')
        return redirect('teacher:exams', request.user.teacher_profile.now_academy.url)
    else:
        return HttpResponseNotFound()


@login_required(login_url='accounts:login')
def create(request):
    if request.user.role != 'Owner' and request.user.role != 'Teacher':
        return HttpResponseNotFound()
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ExamCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if request.user.role == 'Owner':
                academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
                exam = Exam.objects.create(academy=academy, name=data['name'], description=data['description'])
                messages.success(request, 'با موفقیت ساخته شد')
                return redirect('exam:exam_details', exam.id)
            else:
                academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
                exam = Exam.objects.create(academy=academy, name=data['name'], description=data['description'])
                exam.access_teachers.add(request.user)
                exam.save()
                messages.success(request, 'با موفقیت ساخته شد')
                return redirect('exam:exam_details', exam.id)
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
def exam_details(request, id):
    exam = get_object_or_404(Exam, id=id)
    teacher_view = False
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
        if exam.academy != academy or exam.closed:
            return HttpResponseNotFound()
        courses = exam.courses.all()
        tqs = exam.tqs.all().order_by('-create')
        dqs = exam.dqs.all().order_by('-create')
        qs = list(chain(tqs, dqs))
        context = {'exam': exam, 'courses': courses, 'qs': qs, 'tqs': tqs, 'dqs': dqs, 'form': QuestionCreateForm}
        return render(request, 'exam/details.html', context)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        if exam.academy != academy or exam.closed:
            return HttpResponseNotFound()
        courses = exam.courses.all()
        tqs = exam.tqs.all().order_by('-create')
        dqs = exam.dqs.all().order_by('-create')
        qs = list(chain(tqs, dqs))
        context = {'exam': exam, 'courses': courses, 'qs': qs, 'tqs': tqs, 'dqs': dqs, 'form': QuestionCreateForm}
        return render(request, 'teacher/exam_details.html', context)
    else:
        return HttpResponseNotFound()


@login_required(login_url='accounts:login')
@owner_required()
def get_classes(request, id):
    exam = get_object_or_404(Exam, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if exam.academy != academy or exam.closed:
        return HttpResponseNotFound()
    context = {}
    for c in academy.courses.all():
        if c not in exam.courses.all():
            context[c.id] = f'{c.name}'
    return JsonResponse(context)


@login_required(login_url='accounts:login')
@owner_required()
def class_invitation(request, id):
    exam = get_object_or_404(Exam, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if exam.academy != academy or exam.closed:
        return HttpResponseNotFound()
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AddJsDic(request.POST)
        if form.is_valid():
            data = form.cleaned_data['dic'].split(',')
            for i in data:
                if i:
                    course = Courses.objects.filter(id=int(i))
                    if course.exists():
                        exam.courses.add(int(i.replace(',', '')))
                        for c in course:
                            for t in c.teachers.all():
                                exam.access_teachers.add(t.id)
                            for s in c.students.all():
                                exam.access_students.add(s.id)
                        exam.save()
                        messages.success(request, 'با موفقیت دعوت شد')
                    else:
                        messages.error(request, 'لطفا مقدار معتبر وارد کنید ')
                        return redirect(url)
        else:
            messages.warning(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def delete_course(request, exam_id, course_id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=exam_id)
    course = get_object_or_404(Courses, id=course_id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if exam.academy != academy or exam.closed or course not in exam.courses.all():
        return HttpResponseNotFound()
    exam.courses.remove(course)
    for c in course.teachers.all():
        exam.access_teachers.remove(c.id)
    for s in course.students.all():
        exam.access_students.remove(s.id)
    exam.save()
    messages.success(request, 'با موفقیت حذف شد')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def update(request, id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=id)
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if exam.academy != academy or exam.closed:
        return HttpResponseNotFound()
    if request.method == 'POST':
        form = ExamUpdateForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'با موفیت ذخیره شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    else:
        form = ExamUpdateForm(request.POST, instance=exam)
    return redirect(url)


@login_required(login_url='accounts:login')
def question_delete(request, e_id, t_id=None, d_id=None):
    exam = get_object_or_404(Exam, id=e_id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy:
        return HttpResponseNotFound
    if t_id:
        question = get_object_or_404(TQuestion, id=t_id)
        if question in exam.tqs.all():
            question.delete()
            messages.success(request, 'با موفقیت حذف شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    else:
        question = get_object_or_404(DQuestion, id=d_id)
        if question in exam.dqs.all():
            question.delete()
            messages.success(request, 'با موفقیت حذف شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect('exam:exam_details', exam.id)


@login_required(login_url='accounts:login')
def add_t_question(request, id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or exam.closed:
        return HttpResponseNotFound
    if request.method == 'POST':
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            question = TQuestion.objects.create(text=data['text'], level=data['level'])
            exam.tqs.add(question)
            messages.success(request, 'با موفقیت اضافه شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
def add_d_question(request, id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or exam.closed:
        return HttpResponseNotFound
    if request.method == 'POST':
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            question = DQuestion.objects.create(text=data['text'], level=data['level'])
            exam.dqs.add(question)
            messages.success(request, 'با موفقیت اضافه شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
def t_question(request, e_id, t_id):
    exam = get_object_or_404(Exam, id=e_id)
    question = get_object_or_404(TQuestion, id=t_id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or exam.closed or question not in exam.tqs.all():
        return HttpResponseNotFound()
    choices = question.choices()
    context = {'question': question, 'exam': exam, 'choices': choices}
    return render(request, 'exam/t_question.html', context)


@login_required(login_url='accounts:login')
def d_question(request, e_id, t_id):
    exam = get_object_or_404(Exam, id=e_id)
    question = get_object_or_404(DQuestion, id=t_id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or exam.closed or question not in exam.dqs.all():
        return HttpResponseNotFound()
    context = {'question': question, 'exam': exam}
    return render(request, 'exam/d_question.html', context)


@login_required(login_url='accounts:login')
def t_question_delete_img(request, e_id, t_id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=e_id)
    question = get_object_or_404(TQuestion, id=t_id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or exam.closed or question not in exam.tqs.all():
        return HttpResponseNotFound()
    question.image.delete()
    messages.success(request, 'با موفیت حذف شد')
    return redirect(url)


@login_required(login_url='accounts:login')
def delete_choice(request, id):
    url = request.META.get('HTTP_REFERER')
    choice = get_object_or_404(Choices, id=id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if choice.academy != academy:
        return HttpResponseNotFound()
    choice.delete()
    messages.success(request, 'با موفیت حذف شد')
    return redirect(url)


@login_required(login_url='accounts:login')
def add_choice(request, e_id, q_id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=e_id)
    question = get_object_or_404(TQuestion, id=q_id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or question not in exam.tqs.all():
        return HttpResponseNotFound
    if request.method == 'POST':
        form = ChoiceCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['text']
            Choices.objects.create(text=data, academy=academy, question=question)
            messages.success(request, 'با موفقیت اضافه شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
def t_question_update(request, e_id, t_id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=e_id)
    question = get_object_or_404(TQuestion, id=t_id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or question not in exam.tqs.all():
        return HttpResponseNotFound
    if request.method == 'POST':
        form = TQuestionUpdateForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'با موفقیت انجام شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
def d_question_delete_img(request, e_id, d_id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=e_id)
    question = get_object_or_404(DQuestion, id=d_id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or exam.closed or question not in exam.dqs.all():
        return HttpResponseNotFound()
    question.image.delete()
    messages.success(request, 'با موفیت حذف شد')
    return redirect(url)


@login_required(login_url='accounts:login')
def d_question_update(request, e_id, d_id):
    url = request.META.get('HTTP_REFERER')
    exam = get_object_or_404(Exam, id=e_id)
    question = get_object_or_404(DQuestion, id=d_id)
    if request.user.role == 'Owner':
        academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    elif request.user.role == 'Teacher':
        academy = Academy.objects.get(id=request.user.teacher_profile.now_academy.id)
        teacher_view = academy.url
    else:
        return HttpResponseNotFound()
    if exam.academy != academy or question not in exam.dqs.all():
        return HttpResponseNotFound
    if request.method == 'POST':
        form = DQuestionUpdateForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'با موفقیت انجام شد')
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def enable_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    url = request.META.get('HTTP_REFERER')
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if exam.academy != academy:
        return HttpResponseNotFound()
    if exam.active:
        exam.active = False
        exam.save()
        messages.success(request, 'با موفیت غیر فعال شد')
    else:
        if academy.exam_num >= 1:
            if exam.start_time and exam.start_date:
                if exam.time or exam.end_date and exam.end_time:
                    if exam.tqs.count() != 0 or exam.dqs.count() != 0:
                        if exam.courses.count() >= 1:
                            exam.active = True
                            exam.save()
                            academy.exam_num -= 1
                            academy.save()
                            messages.success(request, 'با موفقت فعال شد اما سوالات تشریحی فعلا در دسترس نیستند .')
                        else:
                            messages.warning(request, 'آزمون حد اقل باید شامل یک دوره بشود')
                    else:
                        messages.warning(request, 'آزمون باید حد اقل 1 سوال داشته باشد')
                else:
                    messages.warning(request, 'آزمون تاریخ پایان یا زمان ندارد')
            else:
                messages.warning(request, 'آزمون تاریخ شروع ندارد')
        else:
            messages.warning(request, 'لطفا اشتراک خریداری کنید')
    return redirect(url)


@login_required(login_url='accounts:login')
@owner_required()
def close_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    url = request.META.get('HTTP_REFERER')
    academy = Academy.objects.get(id=request.user.owner_profile.academy.id)
    if exam.academy != academy:
        return HttpResponseNotFound()
    else:
        exam.closed = True
        exam.save()
        messages.success(request, 'آزمون با موفقیت بسته شد')
    return redirect(url)


@login_required(login_url='accounts:login')
def exam_participate(request, id):
    exam = get_object_or_404(Exam, id=id)
    if request.user.role != 'Student':
        return HttpResponseNotFound()
    if not request.user in exam.access_students.all():
        return HttpResponseNotFound()
    context = {'exam': exam}
    return render(request, 'exam/participate.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def exam_analysis(request, id):
    exam = get_object_or_404(Exam, id=id)
    academy = request.user.owner_profile.academy
    if exam.academy != academy or not exam.closed:
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
    return render(request, 'exam/analysis.html', context)


@login_required(login_url='accounts:login')
@owner_required()
def student_analysis(request, e_id, s_id):
    exam = get_object_or_404(Exam, id=e_id)
    student = get_object_or_404(User, id=s_id)
    if exam.academy != request.user.owner_profile.academy:
        return HttpResponseNotFound()
    sheet = get_object_or_404(AnswerSheet, student=student, exam=exam)
    chart = GrowthChart.objects.filter(student=student)
    context = {'sheet': sheet, 'exam': exam, 'chart': chart,'student':student}
    return render(request, 'exam/student_analysis.html', context)
