# Generated by Django 4.2 on 2023-04-22 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_exam_academy'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
