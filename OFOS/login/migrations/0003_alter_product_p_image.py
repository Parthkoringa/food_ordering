# Generated by Django 4.2.10 on 2024-03-04 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_product_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='p_image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
