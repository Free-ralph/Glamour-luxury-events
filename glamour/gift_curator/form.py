from django import forms
from .models import AddOns



FOOD_TRAY = (
    ("B" , "BREAKFAST TRAY") ,
    ("L" , "LUNCH TRAY") ,
    ("D" , "DINNER TRAY") 
)

TYPES = (
    ("M" , "Mini Tray"),
    ("S" , "Standard"),
    ("J" , "Jumbo"),
)

def build_add_on_tuple():
    ADD_ONS = []
    add_on_qs = AddOns.objects.all()
    for add_on in add_on_qs:
        ADD_ONS.append((f"{add_on.value_id}" , f"{add_on.add_on_name}"))
    return tuple(ADD_ONS) 

class FoodTrayForm(forms.Form):
    Tray = forms.ChoiceField(choices=FOOD_TRAY , required=False)
    tray_type = forms.ChoiceField(choices=TYPES, required=False)
    add_ons   = forms.MultipleChoiceField(  choices=build_add_on_tuple() , 
                                            widget=forms.CheckboxSelectMultiple() , 
                                            required=False)

class FruitBaskets(forms.Form):
    basket_type = forms.ChoiceField(choices=TYPES)