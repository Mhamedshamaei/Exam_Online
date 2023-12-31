# Generated by Django 4.2 on 2023-04-27 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plans', '0005_alter_plans_exam_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.fields.CharField, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
