from django.db import models
from django.contrib.auth.models import User
from core.models import Item
# Create your models here.


TRAY_TYPES = (
    ("M" , "Mini"),
    ("S" , "Standard"),
    ("J" , "Jumbo"),
)

FOOD_TRAY = (
    ("B" , "BREAKFAST") ,
    ("L" , "LUNCH") ,
    ("D" , "DINNER") 
)


class AddOns(models.Model):
    add_on_name = models.CharField(max_length=20)
    # value_is a unique identifier like slugs that is used for the backend
    value_id = models.CharField(max_length=2 , help_text="use unique characters, maximum is two")
    discount_price = models.FloatField(blank = True)
    price = models.FloatField()
    class Meta:
        verbose_name_plural = 'add ons'

    def __str__(self):
        return self.add_on_name
    
    def get_price(self):
        if self.discount_price :
            return self.discount_price 
        else :
            return self.price

class TrayAddOns(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    add_on = models.ForeignKey(AddOns , on_delete = models.CASCADE  , blank=True, null=True)
    quantity = models.IntegerField( default=1)
    ordered = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Tray add_ons'
    
    def get_total_price(self):
        return self.quantity * self.add_on.get_price() 

    def __str__(self):
        return f"{self.quantity} of {self.add_on.add_on_name}"
    
class Tray(models.Model):
    category = models.CharField(max_length=20)
    discount_price = models.FloatField(blank=True)
    tray_name = models.CharField(max_length=1 , choices=FOOD_TRAY)
    tray_type = models.CharField(choices=TRAY_TYPES , max_length=1)
    price = models.FloatField()
    food_items = models.TextField()
    def __str__(self):
        return self.tray_name
    
    def get_price(self):
        if self.discount_price :
            return self.discount_price
        else :
            return self.price
        
class GiftItem(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default=False)
    gift_item = models.ForeignKey(Item , on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username 

class TrayItem(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    tray = models.ForeignKey(Tray , on_delete = models.CASCADE)
    add_ons = models.ManyToManyField(TrayAddOns) 

    def get_total_price(self):
        total = 0
        for add_on in self.add_ons.all():
            total += add_on.get_total_price()
        return total + self.tray.get_price()

    def __str__(self):
        return f"{self.tray.get_tray_name_display()} {self.tray.get_tray_type_display()}"   

class TrayCart(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE )
    reference = models.CharField(max_length=10 , blank=True, null=True)#TODO Remember remove null and black
    timestamp = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    tray_item = models.ManyToManyField(TrayItem)

    def __str__(self):
        return self.user.username
        

class GiftBox(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE )
    reference = models.CharField(max_length=10 , blank=True, null=True)#TODO Remember remove null and black
    ordered = models.BooleanField(default=False)
    gift_item = models.ManyToManyField(GiftItem)

    class Meta:
        verbose_name_plural = 'GiftBoxes'
    
    def __str__(self):
        return self.user.username
