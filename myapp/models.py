from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    type=models.CharField(max_length=20,choices=[('admin', 'Admin'), ('user', 'User'), ('seller', 'Seller')], default='user')



class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    id_proof_type = models.CharField(max_length=50)
    id_proof_image = models.ImageField(upload_to='id_proofs/', null=True, blank=True)  
    is_approved = models.BooleanField(default=False)  
    

    def __str__(self):
        return self.user.username



class Product(models.Model):
    CATEGORY_CHOICES = [
        ('accessories', 'Accessories'),
        ('clothing', 'Clothing'),
        ('arts', 'Arts'),
        ('handicrafts', 'Handicrafts'),
        ('all', 'All')
    ]

    

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    image_front = models.ImageField(upload_to='product_images/front', blank=True, null=True)
    image_back = models.ImageField(upload_to='product_images/back', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    added_on = models.DateTimeField(auto_now_add=True)



class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s wishlist - {self.product.name}"

class PasswordReset(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    token=models.CharField(max_length=100,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)



class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    street = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}, {self.street}"



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'), 
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ], default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('canceled', 'Canceled')
        ],
        default='pending')
    seller_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    admin_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 


    def __str__(self):
        return f"{self.quantity} of {self.product.name}"



class Revenue(models.Model):
    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='revenues')
    admin_earning = models.DecimalField(max_digits=10, decimal_places=2) 
    seller_earning = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Revenue from OrderItem {self.order_item.id} - Seller: {self.seller.username}"

