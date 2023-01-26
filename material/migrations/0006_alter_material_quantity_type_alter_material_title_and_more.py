# Generated by Django 4.1.5 on 2023-01-26 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0005_alter_material_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='quantity_type',
            field=models.CharField(choices=[('Adet', 'adet'), ('Kg', 'kg'), ('Gr', 'gr'), ('L', 'l')], default='adet', max_length=30, verbose_name='Birim'),
        ),
        migrations.AlterField(
            model_name='material',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Malzeme İsmi'),
        ),
        migrations.AlterField(
            model_name='material',
            name='type',
            field=models.CharField(choices=[('Diğer', 'diger'), ('Menteşe', 'mentese'), ('Ray', 'ray')], default='diger', max_length=30, verbose_name='Malzeme Tipi'),
        ),
    ]
