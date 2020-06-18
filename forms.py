from django.forms.models import ModelForm
from .models import *

class UserForm(ModelForm):
    class Meta:
        model=User
        fields="__all__"

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields="__all__"

class AddressForm(ModelForm):
    class Meta:
        model=Address
        fields="__all__"

class CommodityForm(ModelForm):
    class Meta:
        model=Commodity
        fields="__all__"

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields="__all__"

class Or_goodsForm(ModelForm):
    class Meta:
        model=Or_goods
        fields="__all__"

