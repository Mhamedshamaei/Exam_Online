# Generated by Django 4.2 on 2023-04-23 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0012_remove_exam_end_remove_exam_start_exam_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dquestion',
            name='create',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='tquestion',
            name='create',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
