# Generated by Django 5.0.1 on 2024-03-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]