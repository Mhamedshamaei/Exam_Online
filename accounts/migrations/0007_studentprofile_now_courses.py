# Generated by Django 4.2 on 2023-04-29 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_studentprofile_now_academy'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='now_courses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.courses'),
        ),
    ]
