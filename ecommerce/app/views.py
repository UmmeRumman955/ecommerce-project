from django.shortcuts import render,redirect
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, PasswordChangeForm,SetPasswordForm) 
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import (Identify,RegisterForm,CheckoutForm)
from django.contrib.auth.decorators import login_required
from .models import (ProductItem, ProductCategory, Product, SizeOption, OrderItem, UserModel,ProductVariation,Address,Order)
from datetime import datetime



# Create your views here.
def registerview(request):
    fm = RegisterForm()
    context = {
        'form' : fm
    }
    if request.method == 'POST':
         fm = RegisterForm(data = request.POST)
         if fm.is_valid():
              email = fm.cleaned_data['email']
              first_name = fm.cleaned_data['first_name']
              last_name = fm.cleaned_data['last_name']
              fm.save()
            #   return HttpResponse('User Created Successfully') 
              messages.success(request, 'user account created successfully')
              return redirect('signin')
    return render(request,'register.html', context)





def signin(request):
     fm = AuthenticationForm()
     context = {
          'form':fm
     }
     if request.method == 'POST':
          fm = AuthenticationForm(data=request.POST)
          if fm.is_valid():
               username = fm.cleaned_data['username']
               password = fm.cleaned_data['password']
               user = authenticate(request, username = username, password=password)
               if user:
                   if user.is_authenticated:  
                    login(request, user)
                    # return HttpResponse('login Successful')
                    messages.success(request,'userlogged in')
                    return redirect('home')
               messages.error(request, 'invalid username and password')
        #   return HttpResponse('Invalid username or password')
     return render(request, 'login.html', context)


@login_required(login_url = '/signin')
def home(request):
    return render(request, 'home.html')


def signout(request):
    logout(request)
    return redirect('signin')

@login_required(login_url = '/signin')
def updatepassword(request):
    username = request.user
    user = User.objects.get(username = username)
    fm = PasswordChangeForm(user)
    context = {
        'form' : fm
    }
    if request.method == "POST":
        fm = PasswordChangeForm(user,data = request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponse('Password Changed')
        return HttpResponse('invalid password')
    return render(request,'pwd_change.html',context)



def identifyview(request):
    fm = Identify()
    context = {
        'form' : fm
    }
    if request.method == 'POST':
        fm = Identify(request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            if User.objects.filter(username = uname).exists():
                url = '/resetpwd/'+uname+'/'
                messages.success(request,'identify the user')
                return redirect(url)
            return redirect('signin')
    return render(request,'identify.html', context)




def resetpwd(request, uname):
    obj = User.objects.get(username = uname)
    fm = SetPasswordForm(obj)
    context = {
        'form' : fm
    }
    if request.method == 'POST':
        fm = SetPasswordForm(obj, data = request.POST)
        if fm.save():
            messages.success(request,'Password reset Successfully')
            return redirect('signin')
        messages.error(request,'New password and confirm password must be same ')      
    return render(request,'resetpwd.html',context)


#fetching all product at a time
def product(request):
    products = ProductItem.objects.all()
    context = {
        'products' : products
    }
    return render(request,'product.html', context)


#fetching single product using id
def singleproduct(request,id):
    if ProductItem.objects.filter(product_item_id =id).exists():
        product = ProductItem.objects.get(product_item_id = id)
        context = {
            'product': product
        }
        return render(request,'singleproduct.html',context)
    return HttpResponse('produc doesnot exist')



#fetching single product using slug (sir method)
# def sglproduct(request, slug):
#     if ProductItem.objects.filter(slug = slug).exists():
#         product = ProductItem.objects.get(slug = slug)
#         context = {
#             'product': product
#         }
#         return render(request,'singleproduct.html',context)
#     return HttpResponse('product doesnot exist')



# fetching single produc using slug
def sglproduct(request, slug):
    product = ProductItem.objects.filter(slug=slug).first()   
    if product:
        context = {
            'product': product
        }
        return render(request, 'singleproduct.html', context)
    return HttpResponse('Product does not exist')



def categoryview(request, slug):
    if ProductCategory.objects.filter(slug = slug).exists():
        category = ProductCategory.objects.get(slug = slug)
        products = Product.objects.filter(product_category__exact = category)
        product_items =  ProductItem.objects.filter(product__in = products)
        context = {
            'products' : product_items
        }
        return render(request, 'category.html', context)
    return HttpResponse('Invalid Category')


def producthomeview(request):
    categories = ProductCategory.objects.filter(category_name__in = ['Mens_Shirt','Womens-Formals','T-shirt', 'Electronics',"Men's Wear"])

    context = {
        'categories': categories
    }
    return render(request,'homes.html', context)


@login_required(login_url = 'signin/')
def add_to_cartview(request, productitemslug, sizeslug):
    username  = request.user
    user = UserModel.objects.get(username = username)
    productitem = ProductItem.objects.get(slug = productitemslug)
    sizeoption = SizeOption.objects.get(slug = sizeslug)

    if OrderItem.objects.filter(user = user, product_item=productitem).exists():
        item = OrderItem.objects.get(user=user, product_item=productitem)
        # item.quantity += 1
        # item.save()
        url = '/increment/'+str(item.id)+'/'
        return redirect(url)
        # return HttpResponse('incremented quantity') 
    OrderItem.objects.create(user=user, product_item= productitem, size=sizeoption)
    return HttpResponse('Product added to cart Successfully')


def increment_quantity(request,id):
    orderitem = OrderItem.objects.get(id=id)
    product_items = ProductItem.objects.get(slug = orderitem.product_item.slug)
    sizeoption = SizeOption.objects.get(slug = orderitem.size.slug)
    product_variation = ProductVariation.objects.get(product_item = product_items,size = sizeoption)

    if orderitem.quantity < product_variation.qty_in_stock:
        orderitem.quantity += 1
        orderitem.save()
        return HttpResponse('quantity incrementted Successfully')
    return HttpResponse('product out of stock')

def dicrement_quantity(request,id):
    orderitem = OrderItem.objects.get(id=id)
    if orderitem.quantity > 1:
        orderitem.quantity -= 1
        orderitem.save()
        return HttpResponse('quantity dicrementted Successfully')
    return HttpResponse('decrement Quantity')

def remove_orderitem(request,id):
    user = UserModel.objects.get(username = request.user)
    if OrderItem.objects.filter(id = id, user=user).exists():
        orderitem = OrderItem.objects.get(id = id, user=user)
        orderitem.delete()
        return HttpResponse('order removed from cart')
    return HttpResponse('item does not exits in cart')


def checkout(request):
    user = UserModel.objects.get(username=request.user)
    checkoutform = CheckoutForm()
    context = {
        'checkoutform': checkoutform
    }
    if request.method == 'POST':
        
        checkoutform = CheckoutForm(request.POST)
        if checkoutform.is_valid():
            use_default_shipping_address = checkoutform.cleaned_data['use_default_shipping_address']

            if use_default_shipping_address and  Address.objects.filter(user=user,address_type='S',default=True).exists():
                shipping_address = Address.objects.get(user=user,address_type='S',default=True)
                    
            else:
                address1 = checkoutform.cleaned_data['shipping_address1']
                address2 = checkoutform.cleaned_data['shipping_address2']
                pincode = checkoutform.cleaned_data['shipping_pincode']
                country = checkoutform.cleaned_data['shipping_country']
                set_default_shipping_address = checkoutform.cleaned_data['set_default_shipping_address']
                if set_default_shipping_address:
                        default = True
                        if Address.objects.filter(user=user,address_type='S',default=True).exists():
                            shipping_address = Address.objects.get(user=user,address_type='S',default=True)
                            shipping_address.default=False
                            shipping_address.save()

                else:
                    default= False

                if address1 and address2 and pincode and country:
                    shipping_address = Address.objects.create(
                                user = user,
                                street_address = address1,
                                apartment_address = address2,
                                country = country,
                                pincode = pincode,
                                address_type = 'S',
                                default = default
                            )
                else:
                    return HttpResponse('Fill the data')
                
            use_default_billing_address = checkoutform.cleaned_data['use_default_billing_address']
            same_billing_address = checkoutform.cleaned_data['same_billing_address']
            if same_billing_address and use_default_shipping_address :
                set_default_billing_address = checkoutform.cleaned_data['set_default_billing_address']
                if set_default_billing_address:
                    default = True
                    if Address.objects.filter(user=user,address_type='B',default=True).exists():
                        billing_address = Address.objects.get(user=user,address_type='B',default=True)
                        billing_address.default=False 
                        billing_address.save()
                else:
                    default= False
                billing_address = Address.objects.create(
                    user = user,
                    street_address = shipping_address.street_address,
                    apartment_address = shipping_address.apartment_address,
                    country = shipping_address.country,
                    pincode = shipping_address.pincode,
                    address_type = 'B',
                    default = default
                )

            elif same_billing_address:
                billing_address = Address.objects.create(
                    user = user,
                    street_address = address1,
                    apartment_address = address2,
                    country = country,
                    pincode = pincode,
                    address_type = 'B',
                    default = default
                )
            
            elif use_default_billing_address and Address.objects.filter(user=user,address_type='B',default=True).exists():
                    billing_address = Address.objects.get(user=user,address_type='B',default=True)
            else:
                address1 = checkoutform.cleaned_data['billing_address1']
                address2 = checkoutform.cleaned_data['billing_address2']
                pincode = checkoutform.cleaned_data['billing_pincode']
                country = checkoutform.cleaned_data['billing_country']
                set_default_billing_address = checkoutform.cleaned_data['set_default_billing_address']
                if set_default_billing_address:
                    default = True
                    if Address.objects.filter(user=user,address_type='B',default=True).exists():
                        billing_address = Address.objects.get(user=user,address_type='B',default=True)
                        billing_address.default=False 
                        billing_address.save()
                else:
                    default= False
                if address1 and address2 and pincode and country:
                    billing_address = Address.objects.create(
                    user = user,
                    street_address = address1,
                    apartment_address = address2,
                    country = country,
                    pincode = pincode,
                    address_type = 'B',
                    default = default
                    )
                else:
                    return HttpResponse('Fill the data')
                       
            cartitems = OrderItem.objects.filter(user_id=user,ordered=False)
            for item in cartitems:
                order = Order.objects.create(
                   user = user,
                   items = item,
                   billing_address= billing_address,
                   shipping_address = shipping_address,
                   ordered_date =  datetime.now()
                )
            return HttpResponse('Do Payment')
        
    return render(request, 'checkout.html',context)