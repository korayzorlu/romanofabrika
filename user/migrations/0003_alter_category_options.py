# Generated by Django 4.1.5 on 2023-02-07 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_usercategory_category_employee_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]
