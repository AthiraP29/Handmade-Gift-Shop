"""
URL configuration for mypro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from myapp import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index,name='index'),
    path('contact-us',views.contactus,name='contact-us'),
    path('checkout',views.checkout,name='checkout'),

    path('admindashboard',views.login,name='admin'),
    path('profile/',views.profile,name='profile'),
    
    path('login/', views.login, name='login'),
    path('accounts/login/', views.login, name='login'),

    path('register/', views.register, name='register'),
    path('check_username/', views.check_username, name='check_username'),

    path('users/', views.user_management, name='user_management'),

    path('product/', views.product_list, name='product_list'),
   
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_detail, name='cart'),
   
    path('products/<int:product_id>/', views.detail, name='product-details'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/cart/<int:product_id>/', views.cartwish, name='cartwish'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishremove/<int:product_id>/', views.wishremove, name='wishremove'),

    path('products/<str:category>/', views.products_by_category, name='products_by_category'),
   
    path('admin-revenue/', views.admin_revenue_management, name='admin_revenue_management'),


    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('update-order-status/<int:item_id>/', views.update_order_status, name='update_order_status'),

    path('products/create/', views.add_product, name='product_create'), 
    path('approve-product/<int:product_id>/', views.approve_product, name='approve_product'),

    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'), 
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),

    
    path('product-quick-view/<int:product_id>/', views.product_quick_view, name='product_quick_view'),


    path('products/', views.add_product, name='product_list'),
    path('users/', views.user_management, name='user_management'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),


    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),
    
    path('logout/', views.logout, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin'),
    path('seller-dashboard/', views.seller_dashboard, name='seller'),
    
    path('about-us',views.aboutus,name='about-us'),
    path('my-account',views.myaccount,name='my-account'),
    path('my-account/', views.myaccount, name='my-account'),  
    path('fetch_orders/', views.fetch_orders, name='fetch_orders'),


    path('checkout/', views.checkout, name='checkout'), 

    path('payment',views.payment,name='payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
  
    path('payment_success/', views.razorpay_success, name='payment_success'),

    path('save-address/', views.save_address, name='save_address'),
    path('razorpay_success/', views.razorpay_success, name='razorpay_success'),


    path('orders/', views.admin_order_management, name='admin_order_management'),
    path('orders/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),

    path('order_details/<int:order_id>/', views.order_details_view, name='order_details'),

    path('delete-order/<int:pk>/', views.delete_order, name='delete_order'),



    path('product-details',views.detail,name='product-details'),
    path('shop/<int:product_id>/', views.detail, name='product-details'),
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
