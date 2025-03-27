from django.contrib import admin
from .models import Product, CartItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_new', 'image')  
    list_filter = ('is_new', 'created_at')  
    search_fields = ('name', 'description')  

# Register models with admin site
admin.site.register(Product, ProductAdmin)  
admin.site.register(CartItem)  