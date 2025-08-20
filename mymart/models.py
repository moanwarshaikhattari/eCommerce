from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    short_discriptions = models.TextField()
    discriptions = models.TextField()
    prd_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock_quantity = models.IntegerField(default=0, blank=False, null=True)
    prd_weight = models.CharField(max_length=50, blank=False, null=True)
    product_slug = AutoSlugField(populate_from='product_name',unique=True,null=True,default=None)
    image_name = models.CharField(max_length=100, blank=True)
    # discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name
    
    @property
    def is_in_stock(self):
        return int(self.stock_quantity) > 0
    
class Review(models.Model):
    product_review = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    # reviewer_name = models.CharField(max_length=100)
    # reviewer_email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review = models.CharField(max_length=500)
    rating = models.IntegerField(default=0)
    post_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.user}({self.rating} stars)"
    
class Add_To_Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart', null=False)
    quantity = models.IntegerField(default=1) #User order Quantity

    def total_price(self):
        return self.product.price * self.quantity



class ShippingDetails(models.Model):
    ship_username = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    ship_address = models.CharField(max_length=200, null=True)
    ship_city = models.CharField(max_length=100, null=True)
    ship_state = models.CharField(max_length=100, null=True)
    ship_zipcode = models.IntegerField(null=True)
    ship_mobile = models.IntegerField(null=True)
    ship_email = models.EmailField(null=True)
    payment_choise = [
        ('cash_deliv', 'Cash On Delivery'),
        ('online', 'Online'),
    ]
    ship_payment_method = models.CharField(max_length=60, choices=payment_choise, default='cash_deliv', null=True)
    order_note = models.CharField(max_length=360, null=True)
    ship_date = models.DateTimeField(auto_now_add=True, null=True)

   