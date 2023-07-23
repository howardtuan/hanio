from django.contrib import admin
from mywebsite.models import *

class MemberAdmin(admin.ModelAdmin):
    list_display =('MID','MName')
    ordering = ('MID',)


class OrderAdmin(admin.ModelAdmin):
    list_display =('okid', 'OID', 'MID', 'PID')
    ordering = ('okid',)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display =('ODID', 'PID', 'OID', 'PNUM','ODate')
    ordering = ('ODID',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('PID', 'PPrice', 'PName', 'Pspec', 'PDetail', 'PStatus', 'PCategory')
    ordering = ('PID',)



class CartAdmin(admin.ModelAdmin):
    list_display = ('CID', 'MID', 'PID', 'NUM')
    ordering = ('CID',)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('managerID', 'username', 'password', 'name')
    ordering = ('managerID',)



admin.site.register(member,MemberAdmin)
admin.site.register(order, OrderAdmin)
admin.site.register(order_detail, OrderDetailAdmin)
admin.site.register(product, ProductAdmin)
admin.site.register(cart, CartAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Favorite)