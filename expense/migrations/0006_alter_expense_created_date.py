# Generated by Django 4.1.5 on 2023-01-31 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0005_alter_expense_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 31, 10, 9, 6, 900772), verbose_name='Tarih'),
        ),
    ]
