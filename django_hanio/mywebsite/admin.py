from django.contrib import admin
from mywebsite.models import *

admin.site.register(member)
admin.site.register(order)
admin.site.register(product)
admin.site.register(cart)