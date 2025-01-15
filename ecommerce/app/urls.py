from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerview,name='register'),
    path('signin/',views.signin,name='signin'),
    path('home/',views.home,name='home'),
    path('signout/',views.signout,name='signout'),
    path('updatepwd/',views.updatepassword,name='updatepassword'),
    path('identify/',views.identifyview,name='identify'),
    path('resetpwd/<str:uname>/',views.resetpwd,name='resetpwd'),
    path('product/',views.product, name='product'),
    path('singleproduct/<int:id>/',views.singleproduct, name='singleproduct'),
    path('sglproduct/<slug>/',views.sglproduct, name='sglproduct'),
    path('category/<slug>/',views.categoryview, name='category'),
    path('producthome/', views.producthomeview, name='producthome'),
    path('addtocart/<productitemslug>/<sizeslug>/',views.add_to_cartview, name = 'addtocart'),
    path('increment/<int:id>/',views.increment_quantity, name = 'increment'),
    path('dicrement/<int:id>/',views.dicrement_quantity, name = 'dicrement'),
    path('remove/<int:id>/',views.remove_orderitem,name ='remove'),
    path('checkout/',views.checkout,name ='checkout'),
]
