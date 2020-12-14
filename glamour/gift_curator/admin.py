from django.contrib import admin
from .models import  Tray ,  GiftBox , GiftItem , TrayItem  , TrayCart , TrayAddOns , AddOns
# Register your models here.


class GiftItemAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'quantity' ,
                    'ordered' , ]

class GiftBoxAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered', ]

class TrayAdmin(admin.ModelAdmin):
    list_display = ['tray_name' ,
                    'tray_type' ]
class TrayCartAdmin(admin.ModelAdmin):
    list_display = ['user' ,
                    'reference' ,
                    'ordered' , ]

class TrayItemAdmin(admin.ModelAdmin):
    list_display = ["__str__" ,
                    "user" ,
                    "ordered" ]

admin.site.register(Tray , TrayAdmin)
admin.site.register( GiftBox )
admin.site.register( GiftItem )
admin.site.register( TrayItem , TrayItemAdmin)
admin.site.register( TrayCart , TrayCartAdmin) 
admin.site.register( TrayAddOns ) 
admin.site.register( AddOns ) 