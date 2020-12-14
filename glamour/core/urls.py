from django.urls import path , include
from .views import  (   HomeView , ProductDetial , Orderdetail , 
                        add_to_cart, update_cart_view , remove_form_cart ,
                        ProductView, add_single_item_to_cart)


app_name = 'core'
urlpatterns = [
    path('' , HomeView.as_view() , name= 'home' ),
    path('product/<slug>/' , ProductDetial.as_view() , name= 'product_detail' ),
    path('products/' , ProductView.as_view() , name= 'product_view' ),
    path('add_to_cart/<slug>/' , add_to_cart , name= 'add_to_cart' ),
    path('add_single_item_to_cart/<slug>/' , add_single_item_to_cart , name= 'add_single_item_to_cart' ),
    path('update_cart_view/<slug>/' , update_cart_view , name= 'update_cart_view' ),
    path('remove_form_cart/<slug>/' , remove_form_cart , name= 'remove_form_cart' ),
    path('cart/' , Orderdetail.as_view() , name= 'cart' ),
]
