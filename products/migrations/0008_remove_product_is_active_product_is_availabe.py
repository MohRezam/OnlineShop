# Generated by Django 5.0.1 on 2024-01-31 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_active',
        ),
        migrations.AddField(
            model_name='product',
            name='is_availabe',
            field=models.CharField(choices=[('available', 'Available'), ('not available', 'Not Available')], default=True, max_length=25),
        ),
    ]