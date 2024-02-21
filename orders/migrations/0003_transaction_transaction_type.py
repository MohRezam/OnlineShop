# Generated by Django 5.0.1 on 2024-02-21 12:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('accounting transactions', 'accounting transactions'), ('receipts', 'receipts')], default=datetime.datetime(2024, 2, 21, 12, 54, 4, 795386, tzinfo=datetime.timezone.utc), max_length=255),
            preserve_default=False,
        ),
    ]