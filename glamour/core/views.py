from django.shortcuts import render , get_object_or_404 , redirect
from django.views.generic import ListView , DetailView , View
from .models import  Coupon , Item , OrderItem , Order 
from .form import QuantityForm , CouponForm , InstructionForm ,Sizes
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.



class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["footer"] =  False
        return context

class ProductDetial(View):
    def get(self , request , slug, *args, **kwargs):
        item = get_object_or_404(Item , slug = slug)
        form = Sizes()
        context = { "item" : item ,
                    "form" : form , 
                    "footer" : False}
        return render(request , "product_detail.html" , context)

class ProductView(ListView):
    model = Item
    template_name = "products.html"
    context_object_name = "items"
    paginate_by = 6
    

class Orderdetail(View):
    def get(self , request , *args, **kwargs):
        if request.user.is_authenticated:
            order_qs = Order.objects.filter( user = request.user ,
                                            ordered = False )

            if order_qs.exists():
                order = order_qs[0]
                footer = False
                if not order.orderitems.exists():
                    footer = True
            else : 
                order = False
                footer = True
            
            context = { "order" : order ,
                    "footer" : footer ,
                    "form" : CouponForm() ,
                    "form_instruct" : InstructionForm()}
            return render(request , 'order_detial.html' , context )
        else :
            context = {"footer" : True}
            return render(request , 'order_detial.html' , context)
        
        
    def post(self , request , *args, **kwargs):
        form = CouponForm(request.POST or None)
        form_instruct = InstructionForm(request.POST or None)
        if form_instruct.is_valid():
            instruction = form_instruct.cleaned_data.get('instruction')
            order_qs = Order.objects.filter(    user = request.user,
                                                ordered = False)
            if order_qs.exists():
                order = order_qs[0]
                if order.instruction:
                    order.instruction += ''.join(f' {instruction}')
                    order.save()
                    messages.success(request , 'instruction(s) has been recieved')
                    return redirect('core:cart')
                order.instruction = instruction
                order.save()
                messages.success(request , 'instruction(s) has been recieved')
                return redirect('core:cart')
            else:
                messages.warning(request , 'you do not have an active order')
                return redirect('core:cart')
        else:
            messages.warning(request , 'Please enter valid instructions')
            return redirect('core:cart')
        if form.is_valid():
            coupon_form = form.cleaned_data.get('coupon')
            try:
                coupon = Coupon.objects.get( title = coupon_form )
                order_qs = Order.objects.filter(   user = request.user, 
                                                    ordered = False)
                if order_qs.exists():
                    order = order_qs[0]
                    order.coupon = coupon
                    if order.coupon.title == coupon_form :
                        messages.warning(request , 'you have already used this coupon')
                        return redirect('core:cart')
                    order.save()
                    messages.success(request , 'Coupon has been successfully activated')
                    return redirect('core:cart')
                else:
                    messages.warning(request , 'Your Order does not exist')
                    return redirect('/')
            except ObjectDoesNotExist :
                messages.warning(request , 'Coupon does not exist')
                return redirect('core:cart')
        else :
            messages.warning(request , 'Please enter valid coupon detail')
            return redirect('core:cart')





# Cart System area
def add_to_cart(request , slug):
    form = QuantityForm(request.POST or None)
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity')
        
        item = get_object_or_404(Item , slug = slug)
        orderitem , created = OrderItem.objects.get_or_create(  user = request.user , 
                                                                item = item,
                                                                ordered = False)
        order_qs = Order.objects.filter(    user = request.user ,
                                            ordered = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item__slug = item.slug).exists():
                orderitem.quantity += quantity
                orderitem.save()
                messages.success(request , "Item quantity has been updated")
                return redirect('core:cart')
            else:
                orderitem.quantity += quantity - 1
                orderitem.save()
                order.orderitems.add(orderitem)
                order.save()
                messages.success(request , 'Item added to cart')
                return redirect('core:cart')
        else:
            order = Order.objects.create(   user = request.user ,
                                            ordered = False)
            orderitem.quantity += quantity - 1
            orderitem.save()
            order.orderitems.add(orderitem)
            order.save()
            messages.success(request , 'item added to cart')
            return redirect('core:cart')
    else:
        messages.warning(request , 'Enter a valid quantity')
        return redirect('core:product_detail' , slug = slug)

def add_single_item_to_cart(request , slug):
    item = get_object_or_404(Item , slug = slug)
    orderitem , created = OrderItem.objects.get_or_create(  user = request.user , 
                                                            item = item,
                                                            ordered = False)
    order_qs = Order.objects.filter(    user = request.user ,
                                        ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item__slug = item.slug).exists():
            orderitem.quantity += 1
            orderitem.save()
            messages.success(request , "Item quantity has been updated")
            return redirect('core:cart')
        else:
            order.orderitems.add(orderitem)
            order.save()
            messages.success(request , 'Item added to cart')
            return redirect('core:cart')
    else:
        order = Order.objects.create(   user = request.user ,
                                        ordered = False)
        order.orderitems.add(orderitem)
        order.save()
        messages.success(request , 'item added to cart')
        return redirect('core:cart')

def update_cart_view(request , slug):
    form = QuantityForm(request.POST or None)
    if form.is_valid():
        quantity = form.cleaned_data.get('quantity')
        try:
            orderitem = OrderItem.objects.get(  user = request.user , 
                                                item__slug = slug,
                                                ordered = False)
            orderitem.quantity = quantity
            orderitem.save()
            messages.success(request , 'Quantity has been updated')
            return redirect('core:cart')
        except ObjectDoesNotExist:
            messages.warning(request , 'oops! an error has occured, please delete and re-add item to cart')
            #TODO feedback page for error occured here //because this kyne error no suppose occur
            return redirect('core:cart')
    else:
        messages.warning(request , 'Enter a valid quantity')
        return redirect('core:cart')

def remove_form_cart(request , slug):
    order_qs = Order.objects.filter(    user = request.user ,
                                        ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        orderitem = OrderItem.objects.get(  user = request.user , 
                                            item__slug = slug,
                                            ordered = False)
        order.orderitems.remove(orderitem)
        orderitem.delete()
        order.save()
        messages.success(request , 'Item removed from cart')
        return redirect('core:cart')
    else:
        messages.warning(request , 'oopps! an unexpcted error occurred plase send us a feedback')
        #TODO feedback page for error occured here //because this kyne error no suppose occur
        return redirect('core:cart')

