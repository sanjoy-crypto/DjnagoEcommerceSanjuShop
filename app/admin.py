from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user','id','name','phone','locality','city']

@admin.register(Product)
class CustomerProduct(admin.ModelAdmin):
    list_display = ['title','id','discounted_price','brand','image_tag']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','id','product','quantity']
    
    
@admin.register(OrderPlaced)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user','customer','id','product','quantity']
