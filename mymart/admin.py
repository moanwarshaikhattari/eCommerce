from django.contrib import admin
from .models import Category, Product, Review, Add_To_Cart, ShippingDetails
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'price', 'prd_weight', 'stock_quantity', 'prd_category', 'short_discriptions', 'image_name', 'created_at']
    search_fields = ['product_name']
    list_editable = ['stock_quantity', 'price', 'image_name', 'prd_weight']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product_review','review','post_at']
   
@admin.register(Add_To_Cart)
class Add_To_CartAdmin(admin.ModelAdmin):
    list_display = ['product','user','quantity']

@admin.register(ShippingDetails)
class ShippingDetailsAdmin(admin.ModelAdmin):
    list_display = ['ship_username', 'ship_mobile', 'ship_email', 'ship_address', 'ship_city', 'ship_state', 'ship_zipcode', 'ship_date']
    list_filter = ['ship_date', 'ship_zipcode', 'ship_email']