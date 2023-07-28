# Generated by Django 4.2 on 2023-05-01 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exam', '0035_exam_student_dones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='student',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='true',
        ),
        migrations.CreateModel(
            name='AnswerSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.answer')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
