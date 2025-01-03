from django.db import models
from django_countries.fields import CountryField


# Create your models here.
class SizeCategory(models.Model):
    category_id = models.AutoField(primary_key=True)   
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class ProductCategory(models.Model):    
    product_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)    
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    category_description = models.TextField(null=True, blank=True)    
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):        
        return self.category_name + ' ' + str(self.size_category)
    

    def save(self, *args, **kwargs):
        self.slug = str(self.category_name).replace(' ', '-')
        super().save(*args, **kwargs)




class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)    
    brand_name = models.CharField(max_length=255)
    brand_description = models.TextField(null=True, blank=True)

    def __str__(self):       
        return self.brand_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)   
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)   
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()   
    model_height = models.FloatField(null=True, blank=True)
    model_wearing = models.CharField(max_length=255, null=True, blank=True)   
    care_instructions = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
  

    def __str__(self):        
        return self.product_name
    
    

class Colour(models.Model):
    colour_id = models.AutoField(primary_key=True)    
    colour_name = models.CharField(max_length=50)

    def __str__(self):
        return self.colour_name


class ProductItem(models.Model):   
    product_item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)   
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    slug = models.CharField(max_length=100, null=True, blank=True)
    image1 = models.ImageField(upload_to='product_images/', blank = True, null=True)
    image2 = models.ImageField(upload_to='product_images/', blank = True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank = True, null=True)
    image4 = models.ImageField(upload_to='product_images/', blank = True, null=True)


    def __str__(self):
        return f"{self.product.product_name} - {self.colour.colour_name}"
    
    def save(self, *args, **kwargs):
        self.slug = str(self.product.product_category) + '-' +str(self.product).replace(' ', '-')
        super().save(*args, **kwargs)

 

class ProductImage(models.Model):   
    image_id = models.AutoField(primary_key=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)    
    image_filename = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product_item}"

class SizeOption(models.Model):    
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=50)    
    sort_order = models.IntegerField()
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE)

    def __str__(self):        
        return self.size_name

class ProductVariation(models.Model):
    variation_id = models.AutoField(primary_key=True)   
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeOption, on_delete=models.CASCADE)
    qty_in_stock = models.IntegerField()

    def __str__(self):       
        return f"{self.product_item} - {self.size.size_name}"
    


  
class UserModel(models.Model): 
    user_id = models.AutoField(primary_key=True) 
    full_name = models.CharField(max_length=100, null=False) 
    username = models.CharField(max_length=50, unique=True, null=False) 
    email = models.EmailField(max_length=255, unique=True, null=False) 
    password_hash = models.CharField(max_length=255, null=False) 
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    profile_picture = models.ImageField(blank=True, null=True) 
    address = models.TextField(blank=True, null=True) 
 
    def __str__(self): 
        return f"{self.username} ({self.full_name})" 
 
 
class OrderItem(models.Model): 
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE) 
    ordered = models.BooleanField(default=False) 
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE) 
    quantity = models.IntegerField(default=1) 
    size = models.ForeignKey(SizeOption, on_delete=models.CASCADE, blank=True, null=True) 
 
    def __str__(self): 
        return f"{self.quantity} x {self.product_item.name} for {self.user.username}" 
 
 
class Address(models.Model): 
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='addresses')  # changed 'address' to 'addresses' 
    street_address = models.CharField(max_length=100, null=False) 
    apartment_address = models.CharField(max_length=100, blank=True, null=True) 
    country = CountryField(null=False) 
    pincode = models.CharField(max_length=100, null=False) 
    address_type = models.CharField(max_length=1, choices=[('B', 'Billing'), ('S', 'Shipping')], null=False) 
    default = models.BooleanField(default=False) 
 
    def __str__(self): 
        return f"{self.street_address}, {self.country.name} ({self.get_address_type_display()})" 
 
class Payment(models.Model): 
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, blank=True, null=True) 
    amount = models.FloatField(null=False) 
    timestamp = models.DateTimeField(auto_now_add=True) 
 
    def __str__(self): 
        return f"Payment of ${self.amount} by {self.user.username if self.user else 'Guest'}" 
 
 
 
 
class Order(models.Model): 
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE) 
    ref_code = models.CharField(max_length=20, blank=True, null=True) 
    items = models.ManyToManyField(OrderItem, blank=True) 
    start_date = models.DateTimeField(auto_now_add=True) 
    ordered_date = models.DateTimeField(null=False) 
    ordered = models.BooleanField(default=False) 
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='shipping_address') 
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='billing_address') 
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)  # Added null=True here 
    being_delivered = models.BooleanField(default=False)   
    received = models.BooleanField(default=False)   
    refund_requested = models.BooleanField(default=False)   
    refund_granted = models.BooleanField(default=False)  
 
    def __str__(self): 
        return f"Order {self.id} by {self.user.username} ({'Completed' if self.ordered else 'Pending'})"