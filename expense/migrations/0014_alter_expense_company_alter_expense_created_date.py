# Generated by Django 4.1.5 on 2023-01-31 19:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0013_alter_company_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.company', verbose_name='Firma'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='created_date',
            field=models.DateField(default=datetime.datetime(2023, 1, 31, 19, 24, 4, 645151, tzinfo=datetime.timezone.utc), verbose_name='Tarih'),
        ),
    ]
