# Generated by Django 4.2 on 2023-04-22 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choices',
        ),
        migrations.DeleteModel(
            name='DQuestion',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.DeleteModel(
            name='TQuestion',
        ),
    ]
