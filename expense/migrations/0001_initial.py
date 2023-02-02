# Generated by Django 4.1.5 on 2023-02-02 09:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Kategori')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Firma')),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Excel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='', verbose_name='Excel Dosyası')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Birim')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Ürün/Hizmet')),
                ('created_date', models.DateField(default=django.utils.timezone.now, verbose_name='Tarih')),
                ('quantity', models.FloatField(default=1, verbose_name='Miktar')),
                ('price', models.FloatField(default=0.0, verbose_name='Birim Fiyat')),
                ('total', models.FloatField(blank=True, null=True)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='expense.category', verbose_name='Kategori')),
                ('company', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='expense.company', verbose_name='Firma')),
                ('unit', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='expense.unit', verbose_name='Birim')),
            ],
        ),
    ]
