# Generated by Django 4.1.5 on 2023-02-28 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0010_alter_loan_completed_installment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='completed_installment',
            field=models.IntegerField(default=0, verbose_name='Tamamlanan Taksitler'),
        ),
    ]