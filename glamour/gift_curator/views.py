from django.shortcuts import render
from .models import GiftBox , Tray  , TrayItem , TrayCart , TrayAddOns , AddOns
from .form import FoodTrayForm
from core.form import QuantityForm
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect , get_object_or_404 
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect



#this function will help us ensure the user doesn't input any value below 1
def is_quantity_valid(quantity):
    valid = True
    if quantity < 1 :
        return False 
    return valid 

# Gift Curating area
class GiftCurating(View):
    def get(self , request , *args, **kwargs):
        gift_box_qs = GiftBox.objects.filter(   user = request.user , 
                                                ordered = False)
        if gift_box_qs.exists():
            gift_box = gift_box_qs[0]
        else :
            gift_box = False
        context = { 'footer' : True ,
                    "gift_box" : gift_box}
        return render(request, 'Gift_curating/base.html' , context)




class GiftBoxArea(LoginRequiredMixin , View):
    def get(self ,  request , *args, **kwargs):
        try :
            gift_box = GiftBox.objects.get( user = request.user , 
                                            ordered = False)
            
            context = { "gift_box" : gift_box}
            return render(request , 'Gift_curating/gift_box_area.html' , context)
        except ObjectDoesNotExist : 
            messages.warning(request , 'you do not have an active gift box, please create')
            return redirect('/')

class TrayCartArea(LoginRequiredMixin , View):
    def get(self ,  request , *args, **kwargs):
        try :
            tray_cart = TrayCart.objects.get(   user = request.user , 
                                                ordered = False)
            context = { "tray_cart" : tray_cart}
            return render(request , 'Gift_curating/tray_cart.html' , context)
        except ObjectDoesNotExist : 
            messages.warning(request , 'you do not have an active Tray Cart, please create')
            return redirect('/')

class EditFoodTray(View):
    def get(self , request , *args, **kwargs):
        tray_item = get_object_or_404(TrayItem , user = request.user , 
                                                 ordered = False ,
                                                 pk = kwargs["pk"])
        # this block of code is to cacth the set of add_ons that weren't selected by the user
        add_on_list = []
        for add_on in AddOns.objects.all() :
            add_on_list.append(add_on)
        for tray_add_on in tray_item.add_ons.all():
            for add_on_items in add_on_list:
                if tray_add_on.add_on.value_id == add_on_items.value_id:
                    add_on_list.remove(add_on_items)
        


        form = FoodTrayForm()
        context = { "tray_item" : tray_item ,
                    "form" : form ,
                    "unselected_add_on" : add_on_list }
        return render(request , "Gift_curating/edit_tray.html" , context)
    def post(self , request , *args, **kwargs):
        context = {'footer' : False}
        form = FoodTrayForm(request.POST or None)
        if form.is_valid():
            tray = form.cleaned_data.get('Tray')
            tray_type = form.cleaned_data.get('tray_type')


            tray_qs = Tray.objects.filter(  tray_name = tray,
                                            tray_type = tray_type)

            if tray_qs.exists():
                tray_item = get_object_or_404(TrayItem ,user = request.user , 
                                                        ordered = False ,
                                                        pk = kwargs["pk"])
                tray = tray_qs[0]
                tray_item.tray = tray
                tray_item.save()
                form = FoodTrayForm()
                context.update({"tray_item" : tray_item , 
                                "form" : form})
                messages.success(request , f"You have changed your tray to {tray.get_tray_name_display()} {tray.get_tray_type_display()} tray")
                return render(request , "Gift_curating/edit_tray.html" , context)
            else :
                messages.warning(request , "Sorry! the selecteed tray does'nt exists")
                return HttpResponseRedirect(request.path_info)
            
        else :
            messages.warning(request , 'your enteries are invalid')
            return HttpResponseRedirect(request.path_info)


@login_required
def create_gift_box(request):
    gift_box , created = GiftBox.objects.get_or_create( user = request.user ,
                                                        ordered = False)
    if created:
        messages.success(request , f'Glamoury gift box for {request.user.username} has been created')
        return redirect('gift:gift_box')
    else :
        messages.warning(request , f'Glamoury gift box for {request.user.username} already exist')
    return redirect('gift:gift_box')

class FoodTray(View):
    def get(self , request , *args, **kwargs):
        form = FoodTrayForm()
        context = { 'form' : form ,
                    'footer' : True}
        return render(request , "Gift_curating/food_tray_form.html" , context)

    def post(self , request , *args, **kwargs):
        context = {'footer' : False}
        # add_on_list = []
        form = FoodTrayForm(request.POST or None)
        if form.is_valid():
            tray = form.cleaned_data.get('Tray')
            tray_type = form.cleaned_data.get('tray_type')


            tray_qs = Tray.objects.filter( tray_name= tray,
                                            tray_type= tray_type)
            if tray_qs.exists():
                tray = tray_qs[0]
                form = FoodTrayForm()
                context.update({"tray" : tray, 
                                "form" : form})
                messages.success(request , f"You selected {tray.get_tray_name_display()} {tray.get_tray_type_display()} tray")
                return render(request , "Gift_curating/food_tray_form.html" , context)
            else :
                messages.warning(request , "Sorry! the selecteed tray does'nt exists")
                return HttpResponseRedirect(request.path_info)
            
        else :
            messages.warning(request , 'your enteries are invalid')
            return HttpResponseRedirect(request.path_info)

@login_required
def add_to_tray_cart(request , pk):
    form = FoodTrayForm(request.POST or None)
    if  form.is_valid():
        add_ons = form.cleaned_data.get('add_ons')
        tray = get_object_or_404(Tray , pk = pk)
        trayitem , created = TrayItem.objects.get_or_create(user = request.user ,  
                                                            tray = tray ,
                                                            ordered = False)
        tray_cart_qs = TrayCart.objects.filter( user = request.user ,
                                                ordered = False)
        if tray_cart_qs.exists():
            if add_ons:
                for value in add_ons:
                    add_ons_obj = AddOns.objects.filter( value_id = value)[0]
                    tray_add_on , created = TrayAddOns.objects.get_or_create(user = request.user ,  
                                                                            add_on = add_ons_obj ,
                                                                            ordered = False)
                    
                    quantity = request.POST[f'quantity_{tray_add_on.add_on.add_on_name}']
                    tray_add_on.quantity = int(quantity)    
                    tray_add_on.save()
                    trayitem.add_ons.add(tray_add_on)
                    trayitem.save()
            tray_cart = tray_cart_qs[0]
            tray_cart.tray_item.add(trayitem)
            tray_cart.save()
            messages.warning(request , "tray has been curated")
            #TODO return redirect to tray cart
            return redirect("gift:tray_cart")
        else : 
            #TODO generate reference
            tray_cart = TrayCart.objects.create(user = request.user ,
                                                ordered = False )
            if add_ons:
                for value in add_ons:
                    add_ons_obj = AddOns.objects.filter( value_id = value)[0]
                    tray_add_on , created = TrayAddOns.objects.get_or_create(user = request.user ,  
                                                                            add_on = add_ons_obj ,
                                                                            ordered = False)
                    quantity = int(request.POST[f'quantity_{tray_add_on.add_on.add_on_name}'])
                    if is_quantity_valid(quantity):
                        tray_add_on.quantity = quantity 
                        tray_add_on.save()
                        trayitem.add_ons.add(tray_add_on)
                        trayitem.save()
                    else :
                        messages.warning(request , f'please make sure {tray_add_on.add_on.add_on_name} input is valid, must be atleast 1')
            tray_cart.tray_item.add(trayitem)
            tray_cart.save()
            messages.success(request , "Your Tray Cart has succesfully been created")
            #TODO return redirect to tray cart
            return redirect("gift:tray_cart")

    else :
        messages.warning(request , 'your enteries are invalid')
        return redirect("gift:food_tray")
    

# this function adds a single add on to the tray_item in the EditTray view
def add_addon(request , pk):
    form = FoodTrayForm(request.POST or None)
    if form.is_valid():
        tray_item_qs = TrayItem.objects.filter(user = request.user,
                                                ordered = False ,
                                                pk = pk)
        add_ons = form.cleaned_data.get('add_ons')
        if tray_item_qs.exists():
            trayitem = tray_item_qs[0]
            for value in add_ons:
                add_ons_obj = AddOns.objects.filter(value_id = value)[0]
                tray_add_on , created = TrayAddOns.objects.get_or_create(user = request.user ,
                                                                            add_on = add_ons_obj,
                                                                            ordered = False)
                quantity = int(request.POST[f"quantity_{tray_add_on.add_on.add_on_name}"])
                if is_quantity_valid(quantity):
                    tray_add_on.quantity = quantity   
                    tray_add_on.save()
                    trayitem.add_ons.add(tray_add_on)
                    trayitem.save()
                else :
                    messages.warning(request , f"{tray_add_on.add_on.add_on_name} wasn't added, make sure it's atleast 1")
            messages.success(request , "added succesfully")
            return redirect("gift:edit_food_tray", pk = pk)
    else :
        messages.warning(request , "invalid input! please try again")
        return redirect("gift:edit_food_tray" , pk = pk)

#This function removes a single add on from the the tray_item in the EditTray view
def remove_addons(request , pk):
    trayitem_qs = TrayItem.objects.filter( user = request.user ,  
                                            ordered = False) 
    tray_add_on = get_object_or_404(TrayAddOns , user = request.user , pk =  pk )
    if trayitem_qs.exists():
        trayitem = trayitem_qs[0]
        trayitem.add_ons.remove(tray_add_on)
        tray_add_on.delete()
        trayitem.save()
        messages.success(request ,  "add on has been removed")
        return redirect('gift:edit_food_tray' , pk = trayitem.pk )
    else:
        messages.warning(request , "Opps something went wrong, we'd fix it")
        return redirect('/')

#This function updates the quantity of collective add_ons already in the tray_item
def update_add_on_quantity(request , pk):
    tray_addons_qs =  TrayAddOns.objects.filter(user = request.user  ,
                                                ordered = False )
    print(tray_addons_qs)
    if tray_addons_qs.exists():
        for tray_add_on in tray_addons_qs:
            quantity = int(request.POST[f"quantity_{tray_add_on.add_on.add_on_name}"])
            print(type(quantity))
            if is_quantity_valid(quantity):
                tray_add_on.quantity = quantity
                tray_add_on.save()
            else :
                messages.warning(request , f"{tray_add_on.add_on.add_on_name}'s input was invalid, make sure it's atleast 1")
        messages.success(request , "add on quantitites has been updated")
        return redirect("gift:edit_food_tray" , pk = pk)
    else:
        messages.warning(request , "Opps something went wrong, we'd fix it")
        return redirect("gift:edit_food_tray" , pk = pk)

#
# def update_add_quantity_view(request , pk):
#     tray_addon_qs = TrayAddOns.objects.filter(  user = request.user ,
#                                                 pk = pk ,
#                                                 ordered = False)
#     if tray_addon_qs.exists():
#         tray_add_on = tray_addon_qs[0]
#         quantity = request.POST[f'quantity_{tray_add_on.add_on.add_on_name}']
#         tray_add_on.quantity = int(quantity) 
#         tray_add_on.save()
#         messages.success(request , "quantity has been updated")
#         return HttpResponseRedirect(request.path_info)
#     else :
#         #TODO send an email to self
#         messages.warning(request , "oops! something went wrong, we'll handle it")
#         return HttpResponseRedirect(request.path_info)
