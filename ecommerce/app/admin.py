from django.contrib import admin
from .models import (
    SizeCategory, ProductCategory, Brand, Product,
    Colour, ProductItem, ProductImage, SizeOption,
    ProductVariation,UserModel,Address,Payment,OrderItem,Order
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1


@admin.register(SizeCategory)
class SizeCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')
    


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('product_category_id', 'category_name', 'size_category', 'parent_category')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_id', 'brand_name')
   


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'product_category', 'brand')


@admin.register(Colour)
class ColourAdmin(admin.ModelAdmin):
    list_display = ('colour_id', 'colour_name')


@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('product_item_id', 'product', 'colour', 'original_price', 'sale_price')
   


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'product_item', 'image_filename')
 


@admin.register(SizeOption)
class SizeOptionAdmin(admin.ModelAdmin):
    list_display = ('size_id', 'size_name', 'sort_order', 'size_category')


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('variation_id', 'product_item', 'size', 'qty_in_stock')



#USer Model
@admin.register(UserModel) 
class UserModelAdmin(admin.ModelAdmin): 
    list_display = ['phone_number'] 
 
@admin.register(Address) 
class AddressAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user', 'street_address', 'apartment_address', 'country', 'pincode', 'address_type', 'default'] 
 
@admin.register(Payment) 
class PaymentAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user', 'amount', 'timestamp', 'stripe_charge_id'] 
 
     
 
@admin.register(OrderItem) 
class OrderItemAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user', 'product_item', 'quantity', 'ordered'] 
    
 
@admin.register(Order) 
class OrderAdmin(admin.ModelAdmin): 
    list_display = [ 
        'id', 'user', 'start_date','ordered_date','ordered', 'being_delivered',  
        'received', 'refund_requested', 'refund_granted' 
    ]
    
