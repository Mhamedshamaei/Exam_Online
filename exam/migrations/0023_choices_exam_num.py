# Generated by Django 4.2 on 2023-04-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0022_choices_academy'),
    ]

    operations = [
        migrations.AddField(
            model_name='choices',
            name='exam_num',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]