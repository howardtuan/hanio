# Generated by Django 4.0 on 2023-06-02 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mywebsite', '0003_product_pspec_alter_cart_cid_alter_member_maddr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='CID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]