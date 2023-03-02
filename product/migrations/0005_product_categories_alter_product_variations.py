# Generated by Django 4.1.5 on 2023-03-02 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.JSONField(blank=True, null=True, verbose_name='Kategoriler'),
        ),
        migrations.AlterField(
            model_name='product',
            name='variations',
            field=models.JSONField(blank=True, null=True, verbose_name='Varyasyonlar'),
        ),
    ]
