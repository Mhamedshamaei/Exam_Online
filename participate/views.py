from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from exam.models import Exam
from courses.forms import *
from django.contrib import messages
from exam.models import *
from django.utils import timezone


@login_required(login_url='accounts:login')
def load_exam(request, id):
    if request.user.role != 'Student':
        return HttpResponseNotFound()
    exam = get_object_or_404(Exam, id=id)
    if not request.user in exam.access_students.all():
        return HttpResponseNotFound()
    context = {'exam': exam}
    return render(request, 'participate/load.html', context)


@login_required(login_url='accounts:login')
def send(request, id):
    if request.user.role != 'Student':
        return HttpResponseNotFound()
    if request.user.role != 'Student':
        return HttpResponseNotFound()
    exam = get_object_or_404(Exam, id=id)
    if not request.user in exam.access_students.all():
        return HttpResponseNotFound()
    if request.method == 'POST':
        form = AddJsDic(request.POST)
        if form.is_valid():
            data = form.cleaned_data['dic'].split(',')
            sheet = AnswerSheet.objects.create(student=request.user, exam=exam)
            exam.student_dones.add(request.user)
            exam.access_students.remove(request.user)
            for i in data:
                if i:
                    ar = i.replace('{', '').replace('}', '').split(':', 1)
                    if ar[0].isdigit():
                        question = get_object_or_404(TQuestion, id=ar[0])
                        answer = ar[1]
                        is_yes = Answer.objects.filter(student=request.user, question=question)
                        if is_yes.exists():
                            is_yes.delete()
                        an = Answer.objects.create(student=request.user, question=question, select=answer, )
                        sheet.answers.add(an.id)
            GrowthChart.objects.create(total=sheet.get_total(), date=timezone.now().date(), student=request.user)
        else:
            messages.error(request, 'لطفا مقدار صحیح وارد کنید')
    return redirect('student:l_exam', request.user.student_profile.now_academy.url)
