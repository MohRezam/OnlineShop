# Generated by Django 5.0.1 on 2024-01-31 19:41

import core.utils
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': 'comments'},
        ),
        migrations.AlterModelOptions(
            name='discount',
            options={'verbose_name_plural': 'discounts'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'products'},
        ),
        migrations.AlterModelOptions(
            name='productfeature',
            options={'verbose_name_plural': 'features'},
        ),
        migrations.AlterModelOptions(
            name='productfeaturevalue',
            options={'verbose_name_plural': 'feature values'},
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.category_image_path),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='products.category'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='type',
            field=models.CharField(choices=[('percentage', 'Percentage'), ('decimal', 'Decimal')], max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.utils.product_image_path),
        ),
    ]