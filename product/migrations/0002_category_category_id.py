# Generated by Django 4.1.5 on 2023-03-01 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_id',
            field=models.IntegerField(default=0, verbose_name='Kategori ID'),
        ),
    ]
