# Generated by Django 4.2 on 2023-04-27 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0007_coupon_remove_order_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='exam_num',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]