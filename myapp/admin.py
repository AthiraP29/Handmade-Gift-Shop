from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([
    Product,
    CustomUser,
    Address,
    Order,
    OrderItem,
    CartItem,
    PasswordReset,
    SellerProfile,
    Wishlist
])

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'seller', 'seller_earning', 'admin_earning', 'created_at')
    search_fields = ('order_item__product__name', 'seller__username') 
