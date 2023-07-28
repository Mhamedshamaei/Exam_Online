from django.db import models
from accounts.models import *
from django.urls import reverse


class Exam(models.Model):
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
    start_time = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    negative = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    courses = models.ManyToManyField(Courses, related_name='exam_courses')
    tqs = models.ManyToManyField('TQuestion', related_name='Exam_TQuestion')
    dqs = models.ManyToManyField('DQuestion', related_name='Exam_DQuestion')
    access_teachers = models.ManyToManyField(User, related_name='exam_t_access')
    access_students = models.ManyToManyField(User, related_name='exam_s_access')
    student_dones = models.ManyToManyField(User, related_name='exam_s_done')

    def __str__(self):
        return self.name


class TQuestion(models.Model):
    QLevel = (
        ('آسان', 'آسان'),
        ('متوسط', 'متوسط'),
        ('سخت', 'سخت'),
    )
    text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='exam_images/', null=True, blank=True)
    level = models.CharField(max_length=100, choices=QLevel, )
    true = models.IntegerField(null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True, null=True)
    is_left = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def choices(self):
        return Choices.objects.filter(question_id=self.id)


class DQuestion(models.Model):
    DLevel = (
        ('آسان', 'آسان'),
        ('متوسط', 'متوسط'),
        ('سخت', 'سخت'),
    )
    text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='exam_images/', null=True, blank=True)
    level = models.CharField(max_length=100, choices=DLevel)
    create = models.DateTimeField(auto_now_add=True, null=True)
    is_left = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Choices(models.Model):
    question = models.ForeignKey(TQuestion, on_delete=models.CASCADE)
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class AnswerSheet(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answers = models.ManyToManyField('Answer', related_name='sheet_answers', null=True, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam.name

    def get_true(self):
        true = 0
        for i in self.answers.all():
            if i.select == i.question.true:
                true += 1
        return true

    def get_false(self):
        false = 0
        for i in self.answers.all():
            if i.select != i.question.true:
                false += 1
        return false

    def get_total(self):
        return int(100 * (self.get_true() / self.answers.all().count()))


class Answer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(TQuestion, on_delete=models.CASCADE, null=True)
    select = models.PositiveIntegerField(null=True)
    true = models.BooleanField(default=False)

    def __str__(self):
        return self.question.text


class GrowthChart(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    total = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.student.email_phone
