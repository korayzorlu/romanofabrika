# Generated by Django 4.1.5 on 2023-03-02 08:30

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_product_special_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Ürün Açıklaması'),
        ),
    ]
