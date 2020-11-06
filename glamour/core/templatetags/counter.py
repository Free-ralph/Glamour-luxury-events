from django import template
from core.models import Order
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter
def counter(user):
    if user.is_authenticated:
        try:
            order = Order.objects.get(  user = user ,
                                        ordered = False)
            return order.orderitems.count()
        except ObjectDoesNotExist:
            return 0
    return 0
        