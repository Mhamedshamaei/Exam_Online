# Generated by Django 4.2 on 2023-05-02 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0037_answer_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answersheet',
            name='answers',
        ),
        migrations.AddField(
            model_name='answersheet',
            name='answers',
            field=models.ManyToManyField(blank=True, null=True, related_name='sheet_answers', to='exam.answer'),
        ),
    ]
