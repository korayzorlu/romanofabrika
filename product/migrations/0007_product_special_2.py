# Generated by Django 4.1.5 on 2023-03-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_descripiton_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='special_2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Özel Alan 2'),
        ),
    ]
