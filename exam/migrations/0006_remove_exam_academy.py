# Generated by Django 4.2 on 2023-04-23 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_exam_closed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='academy',
        ),
    ]
