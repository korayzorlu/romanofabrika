# Generated by Django 4.1.5 on 2023-02-07 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_category_options'),
    ]

    operations = [
        migrations.RenameModel("Category", "UserCategory")
    ]