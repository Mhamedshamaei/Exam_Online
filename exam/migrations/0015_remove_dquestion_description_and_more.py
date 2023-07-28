# Generated by Django 4.2 on 2023-04-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0014_alter_dquestion_level_alter_tquestion_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dquestion',
            name='description',
        ),
        migrations.RemoveField(
            model_name='dquestion',
            name='direction',
        ),
        migrations.RemoveField(
            model_name='tquestion',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tquestion',
            name='direction',
        ),
        migrations.AddField(
            model_name='dquestion',
            name='is_left',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tquestion',
            name='is_left',
            field=models.BooleanField(default=False),
        ),
    ]