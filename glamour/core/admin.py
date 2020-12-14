from django.contrib import admin
from .models import (Item , OrderItem , Order , Coupon)
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user' ,
                    'ordered' ,]
    list_filter = [ 'user' ,
                    'ordered',]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user' ,
                    'quantity' ,
                    'ordered' ,]
    list_filter = [ 'user' ,
                    'ordered',]

class CouponAdmin(admin.ModelAdmin):
    list_display = [    'title' ,
                        'discount' ,]


admin.site.register(Item)
admin.site.register(Order , OrderAdmin)
admin.site.register( OrderItem ,OrderItemAdmin )
admin.site.register( Coupon , CouponAdmin)
