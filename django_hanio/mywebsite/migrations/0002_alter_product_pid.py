# Generated by Django 4.0 on 2023-06-27 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mywebsite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='PID',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='產品編號'),
        ),
    ]
