from django.contrib import admin
from mywebsite.models import *

class MemberAdmin(admin.ModelAdmin):
    list_display =('MID','MName')
    ordering = ('MID',)

admin.site.register(member,MemberAdmin)
admin.site.register(order)
admin.site.register(product)
admin.site.register(cart)



