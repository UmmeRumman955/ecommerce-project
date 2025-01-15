from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserModel


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'username','password1', 'password2']

class loginform(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100,widget = forms.PasswordInput())
              

class Identify(forms.Form):
    username = forms.CharField(max_length = 100)

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CheckoutForm(forms.Form):
    shipping_address1 = forms.CharField(max_length=100, required=False)
    shipping_address2 = forms.CharField(max_length=100, required=False)
    shipping_country = forms.CharField(max_length=100, required=False)

    shipping_pincode = forms.IntegerField(required=False)
    set_default_shipping_address = forms.BooleanField(required=False)
    use_default_shipping_address = forms.BooleanField(required=False)


    same_billing_address = forms.BooleanField(required=False)
    billing_address1 = forms.CharField(max_length=100, required=False)
    billing_address2 = forms.CharField(max_length=100, required=False)
    billing_country = forms.CharField(max_length=100, required=False)

    
    billing_pincode = forms.IntegerField(required=False)
    set_default_billing_address = forms.BooleanField(required=False)
    use_default_billing_address = forms.BooleanField(required=False)


