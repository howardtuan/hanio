from django.contrib import admin
from mywebsite.models import *

class MemberAdmin(admin.ModelAdmin):
    list_display =('MID','MName')
    ordering = ('MID',)

admin.site.register(member,MemberAdmin)
admin.site.register(order)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('PID', 'PPrice', 'PName', 'Pspec', 'PDetail', 'PStatus', 'PCategory')
    ordering = ('PID',)

admin.site.register(product, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('CID', 'MID', 'PID', 'NUM')
    ordering = ('CID',)

admin.site.register(cart, CartAdmin)