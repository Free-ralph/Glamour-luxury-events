from django.urls import path 
from .views import (GiftCurating , create_gift_box , GiftBoxArea , FoodTray , 
                    add_to_tray_cart , TrayCartArea , EditFoodTray , update_add_on_quantity,
                    remove_addons , add_addon)

app_name = "gift"
urlpatterns = [
    path('' , GiftCurating.as_view() , name= 'gift_curating' ),
    path('create_gift_box/' , create_gift_box , name= 'create_gift_box' ),
    path('gift-box/' , GiftBoxArea.as_view() , name= 'gift_box' ),
    path('tray-cart/' , TrayCartArea.as_view() , name= 'tray_cart' ),
    path('tray-cart/edit/<int:pk>/' , EditFoodTray.as_view() , name= 'edit_food_tray' ),
    path('tray-cart/edit/remove/<int:pk>/' , remove_addons , name= 'remove_addons' ),
    path('update_add_on_quantity/<int:pk>/' , update_add_on_quantity , name= 'update_add_on_quantity' ),
    path('gift-box/add_to_tray_cart/<int:pk>/' , add_to_tray_cart , name= 'add_to_tray_cart' ),
    path('gift-box/add_on/<int:pk>/' , add_addon , name= 'add_addon' ),
    path('gift-box/food-tray/' , FoodTray.as_view() , name= 'food_tray' ),
]