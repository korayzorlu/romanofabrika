# Generated by Django 4.1.5 on 2023-01-30 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0012_remove_material_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]
