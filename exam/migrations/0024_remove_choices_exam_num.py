# Generated by Django 4.2 on 2023-04-27 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0023_choices_exam_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choices',
            name='exam_num',
        ),
    ]
