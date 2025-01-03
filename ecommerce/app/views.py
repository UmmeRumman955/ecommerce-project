from django.shortcuts import render,redirect
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, PasswordChangeForm,SetPasswordForm) 
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import Identify,RegisterForm
from django.contrib.auth.decorators import login_required
from .models import ProductItem, ProductCategory, Product


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
    categories = ProductCategory.objects.filter(category_name__in = ['Mens_Shirt','Womens-Formals','T-shirt'])

    context = {
        'categories': categories
    }
    return render(request,'homes.html', context)


