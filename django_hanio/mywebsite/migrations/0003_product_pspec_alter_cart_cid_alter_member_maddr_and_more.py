# Generated by Django 4.1.3 on 2023-06-02 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mywebsite", "0002_alter_cart_num"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="Pspec",
            field=models.IntegerField(default=0, verbose_name="產品規格"),
        ),
        migrations.AlterField(
            model_name="cart",
            name="CID",
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name="member",
            name="MAddr",
            field=models.CharField(max_length=100, null=True, verbose_name="會員地址"),
        ),
        migrations.AlterField(
            model_name="member",
            name="MCK",
            field=models.CharField(max_length=100, null=True, verbose_name="信用卡到期日"),
        ),
        migrations.AlterField(
            model_name="member",
            name="MID",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="會員編號"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="PNUM",
            field=models.IntegerField(verbose_name="數量"),
        ),
    ]