from django import forms


PILLOW_SIZES = (
    ('F' , '16inches') ,
    ('S' , '18inches') ,
    ('T' , '20inches') 
)

class QuantityForm(forms.Form):
    quantity = forms.IntegerField()

class InstructionForm(forms.Form):
    instruction = forms.CharField( widget = forms.Textarea(
        attrs = {   'cols' : "30" ,
                    "rows" : "2" ,
                    "class" : "form-control"}))

class CouponForm(forms.Form):
    coupon = forms.SlugField( widget = forms.TextInput(
        attrs = {   'placeholder' : 'Apply coupon ',
                    'aria-describedby': 'button-addon3', 
                    'class':"form-control border-0" ,}))

class Sizes(forms.Form):
    sizes = forms.ChoiceField(choices=PILLOW_SIZES)

