# Generated by Django 4.1.5 on 2023-02-17 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cargo_address',
            field=models.JSONField(default=1, verbose_name='Teslimat'),
            preserve_default=False,
        ),
    ]