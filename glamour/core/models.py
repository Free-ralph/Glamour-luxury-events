from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Item(models.Model):
    category = models.CharField(max_length=40)
    title = models.CharField(max_length=40)
    slug = models.SlugField(help_text="Should be a unique name of the product")
    discount_price = models.FloatField( blank=True  ,null = True )
    description = models.TextField(blank=True  ,null = True )
    price = models.FloatField()
    image = models.ImageField( default = "product_images/default-01.jpg")
    whishlist = models.BooleanField(default=False)

    def get_price(self):
        price = self.price
        if self.discount_price:
            price = self.discount_price
        return price

    def __str__(self):
        return self.title

class AddOns(models.Model):
    add_on_name = models.CharField(max_length=20)
    price = models.FloatField()
    
    def __str__(self):
        return self.add_on_name
    
class Trays(models.Model):
    category = models.CharField(max_length=20)
    tray_name = models.CharField(max_length=20)
    price = models.FloatField()
    food_items = models.TextField()
    add_ons = models.ManyToManyField(AddOns)

    class Meta:
        verbose_name_plural = 'Trayes'
    def __str__(self):
        return self.tray_name

class GiftItem(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)
    gift_item = models.ForeignKey(Item , on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username 

class GiftTray(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)
    gift_tray = models.ForeignKey(Trays , on_delete = models.CASCADE)

class GiftBox(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE )
    reference = models.CharField(max_length=10 , blank=True, null=True)#TODO Remember remove null and black
    ordered = models.BooleanField(default=False)
    gift_item = models.ManyToManyField(GiftItem)

    class Meta:
        verbose_name_plural = 'GiftBoxes'
    
    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item , on_delete = models.CASCADE)

    def get_total_price(self):
        return self.quantity * self.item.get_price()

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'
        
class Coupon(models.Model):
    title = models.SlugField(max_length=15)
    discount = models.FloatField()

    def __str__(self):
        return self.title

# class Whishlist(models.Model):
#     user = models.ForeignKey(User  , on_delete = models.CASCADE)
#     items = models.ManyToManyField(Item) 

#     def __str__(self):
#         return self.user

class Order(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE )
    reference = models.CharField(max_length=10 , blank=True, null=True)#TODO Remember remove null and black
    ordered = models.BooleanField(default=False)
    orderitems = models.ManyToManyField(OrderItem)
    delivery_fee = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon , on_delete=models.SET_NULL , blank=True, null=True)
    instruction = models.TextField(blank=True, null=True)

    def get_summed_price(self):
        total = 0
        for orderitem in self.orderitems.all():
            total += orderitem.get_total_price()
        return total

        
    def get_total_price(self):
        total = self.get_summed_price()
        if self.delivery_fee:
            total = self.get_summed_price() + self.delivery_fee
            if self.coupon:
                total -= self.coupon.discount
            return total
        if self.coupon:
                total -= self.coupon.discount
        return total


    def __str__(self):
        return self.user.username