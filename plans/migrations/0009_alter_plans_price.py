# Generated by Django 4.2 on 2023-04-27 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0008_order_exam_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plans',
            name='price',
            field=models.PositiveIntegerField(max_length=100),
        ),
    ]
