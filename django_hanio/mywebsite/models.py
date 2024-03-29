from django.db import models
from django.utils import timezone
from django import forms


now = timezone.now

class member(models.Model):
    MID = models.AutoField('會員編號', primary_key=True)
    MName = models.CharField('會員姓名', max_length=20, null=False)
    MPhone = models.CharField('會員電話', max_length=50, null=False)
    MPW = models.CharField('會員密碼', max_length=20, null=False)
    MAccount = models.CharField('會員帳號', max_length=50, null=False)
    MEmail = models.CharField('會員信箱', max_length=100, null=False)
    MAddr = models.CharField('會員地址', max_length=100, null=True)
    MVISA = models.CharField('會員信用卡號', max_length=100, null=True)
    MCK = models.CharField('信用卡到期日', max_length=100, null=True)

    # def __str__(self) -> str:
    #     return self.MID


class order(models.Model):
    okid = models.AutoField(primary_key=True)
    OID = models.IntegerField('訂單編號')
    MID = models.CharField('會員編號', max_length=1000)
    PID = models.CharField('產品編號', max_length=1000)




class order_detail(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', '貨到付款'),
        ('CC', '刷卡'),
        ('CVS', '超商'),
    ]

    ORDER_STATUS_CHOICES = [
        ('NOT_SHIPPED', '尚未出貨'),
        ('SHIPPED', '已出貨'),
        ('ARRIVED', '已抵達'),
    ]
    ODID = models.AutoField('訂單明細編號', primary_key=True)
    OID = models.IntegerField('訂單編號')
    MID = models.CharField('會員編號', max_length=1000)
    PID = models.CharField('產品編號', max_length=1000)
    PNUM = models.IntegerField('數量')
    # OMail = models.CharField('訂單者信箱', max_length=1000)
    ODate = models.DateField('訂單日期', auto_now_add=True)
    OAddr = models.CharField('配送地址', max_length=100)
    OStatus = models.CharField('訂單狀態',max_length=12, choices=ORDER_STATUS_CHOICES, default='NOT_SHIPPED')
    OPayment = models.CharField('付款方式',max_length=3, choices=PAYMENT_METHOD_CHOICES, default='COD')


class product(models.Model):
    PRODUCT_STATUS_CHOICES = [
        ('IN_STOCK', '上架'),
        ('OUT_OF_STOCK', '下架'),
        ('UNAVAILABLE', '缺貨'),
    ]
    PID = models.AutoField('產品編號', primary_key=True)
    PPrice = models.IntegerField('產品價錢')
    PName = models.CharField('產品名稱', max_length=100)
    PDetail = models.CharField('產品內容', max_length=10000)
    Pspec = models.IntegerField('產品規格',default=0)
    Pnum = models.IntegerField('產品數量',default=0)
    PStatus = models.CharField('產品狀態', max_length=13, choices=PRODUCT_STATUS_CHOICES, default='IN_STOCK')
    PPhoto = models.ImageField('產品圖片', upload_to='product_images/', blank=True, null=True)
    PCategory = models.CharField('產品分類', max_length=20) #也可以用選項


class cart(models.Model):
    CID = models.AutoField(primary_key=True)
    MID = models.CharField('會員編號', max_length=1000)
    PID = models.CharField('產品編號', max_length=1000 )
    NUM = models.IntegerField('數量')

class Manager(models.Model):
    managerID = models.AutoField(primary_key=True)
    username = models.CharField('使用者名稱', max_length=100, unique=True)
    password = models.CharField('密碼', max_length=100)
    name = models.CharField('姓名', max_length=100)
    created_at = models.DateTimeField('建立時間', auto_now_add=True)

class fav(models.Model):
    FID = models.AutoField(primary_key=True)
    MID = models.CharField('會員編號', max_length=1000)
    PID = models.CharField('產品編號', max_length=1000 )