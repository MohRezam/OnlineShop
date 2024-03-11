# Generated by Django 5.0.1 on 2024-03-11 13:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_coupon_code_alter_coupon_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='coupon',
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.IntegerField(db_column='discount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(90)]),
        ),
    ]
