# Generated by Django 4.1.5 on 2023-02-28 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0016_alter_loan_installment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='installment_status',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.SET_DEFAULT, to='loan.installmentstatus', verbose_name='Taksit Durumu'),
        ),
    ]
