# Generated by Django 4.0 on 2023-05-25 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mywebsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='NUM',
            field=models.IntegerField(verbose_name='數量'),
        ),
    ]
