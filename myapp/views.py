from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages,auth
from .models import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from email_validator import validate_email, EmailNotValidError
from decimal import Decimal
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.conf import settings
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO







# Create your views here.



def add_to_cart(request, product_id):
    if request.user.is_authenticated:  
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)

            if request.user == product.seller:
                messages.error(request, "You cannot purchase your own product.")
                return redirect('products_by_category', category='all')  

            if CartItem.objects.filter(product=product, user=request.user).exists():
                cart_item = CartItem.objects.get(product=product, user=request.user)
                cart_item.quantity += 1
                cart_item.save()
            else:
                CartItem(product=product, quantity=1, user=request.user).save()
                messages.success(request, f'Added {product.name} to your cart.')

            return redirect(request.META.get('HTTP_REFERER', 'shop-show-subcategories'))
        else:
            messages.error(request, 'Product not found.')
            return redirect('products_by_category', category='all') 
    else:
        messages.warning(request, 'Please log in to add items to your cart.')
        return redirect('login')



def cartwish(request, product_id):
    if request.user.is_authenticated:  
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)

            if request.user == product.seller:
                messages.error(request, "You cannot purchase your own product.")
                return redirect('wishlist') 

            if CartItem.objects.filter(product=product, user=request.user).exists():
                cart_item = CartItem.objects.get(product=product, user=request.user)
                cart_item.quantity += 1
                cart_item.save()
            else:
                CartItem.objects.create(product=product, quantity=1, user=request.user)
                messages.success(request, f'Added {product.name} to your cart.')

            return redirect('wishlist') 
        else:
            messages.error(request, 'Product not found.')
            return redirect('wishlist') 
    else:
        messages.warning(request, 'Please log in to add items to your cart.')
        return redirect('login') 


def cart_detail(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to view your cart.')

        return redirect('login')  

    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if cart_items.exists():
        item_totals = [{
            'item': cart_item,
            'total_price': cart_item.quantity * cart_item.product.price
        } for cart_item in cart_items]
        total_amount = sum([i['total_price'] for i in item_totals])
    else:
        item_totals = None
        total_amount = 0

    cart_is_empty = not cart_items.exists()  
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            return redirect('cart')

        if quantity < 1:
            print("Quantity received:", quantity) 
            return redirect('cart')

        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            product = cart_item.product

            if quantity > product.stock:
                messages.error(request, f"Cannot add {quantity}. Only {product.stock} available.")
                print("Quantity received:", quantity)  
                return redirect('cart')

            if quantity == 0:
                cart_item.delete()
                if CartItem.objects.filter(user=request.user).exists():
                    messages.success(request, 'Product removed from cart successfully.')
                
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated successfully.')
                print("Quantity received:", quantity)  

        except CartItem.DoesNotExist:
            return redirect('cart')

        return redirect('cart')

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'item_totals': item_totals,
        'total_amount': total_amount,
        'cart_is_empty': cart_is_empty,  
        'wishlist_count': wishlist_count,  
    })




def remove_from_cart(request, product_id):
    try:
        cart_item = CartItem.objects.get(user=request.user, product__id=product_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        messages.error(request, 'Product not in cart.')

    return redirect('cart')



@login_required
def product_list(request):
    user = request.user

    if user.is_superuser:
        products = Product.objects.all() 
        return render(request, 'admindashboard.html', {'products': products, 'active_nav': 'products'})
    else:
        products = Product.objects.filter(seller=user)  
        return render(request, 'seller.html', {'products': products, 'active_nav': 'products'})

def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You need to log in to add items to your wishlist.'}, status=403)

    try:
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if created:
            return JsonResponse({'status': 'added'})
        else:
            return JsonResponse({'status': 'exists'}, status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def wishremove(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
        
        if wishlist_item.exists():
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        else:
            return JsonResponse({'status': 'not_found'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def remove_from_wishlist(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
        
        if wishlist_item.exists():
            wishlist_item.delete()
            
        else:
            messages.info(request, f'{product.name} is not found in your wishlist.')

    except Exception as e:
        messages.error(request, f'Error removing from wishlist: {str(e)}')

    return redirect('wishlist') 

def wishlist_view(request):
    if not request.user.is_authenticated:
        messages.info(request, "Your wishlist is waiting! Log in to start adding.")
        return redirect('login')  

    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    wishlist_products = [item.product for item in wishlist_items]  # Extract products from wishlist items
    cart_items = CartItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'wishlist.html', {
        'wishlist_products': wishlist_products,
        'cart_items': cart_items,
        'wishlist_count': wishlist_count,


    })

def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)


    cart_items = []
    wishlist_products = []
    wishlist_count = 0  

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).values_list('product__id', flat=True)
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product__id', flat=True)
        wishlist_count = Wishlist.objects.filter(user=request.user).count()  


    return render(request, 'product-details.html', {
        'product': product,
        'cart_items': cart_items,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count, 

    })


def product_quick_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True, is_deleted=False)

    product_data = {
        'name': product.name,
        'price': float(product.price),
        'description': product.description,
        'stock': product.stock,
        'category': product.get_category_display(), 
        'image_front': product.image_front.url if product.image_front else None,  
        'image_back': product.image_back.url if product.image_back else None,   
    }

    return JsonResponse(product_data)


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image_front = request.FILES.get('image_front')
        image_back = request.FILES.get('image_back')
        
        seller = request.user

        product = Product.objects.create(
            name=name,
            description=description,
            category=category,
            price=price,
            stock=stock,
            seller=seller,
            image_front=image_front,
            image_back=image_back,
            is_approved=False  
        )

        return HttpResponseRedirect(f'{reverse("seller_dashboard")}?product_added=true')


    
    return render(request, 'product_create.html')


@login_required
def approve_product(request, product_id):
    if request.user.is_superuser:
        product = get_object_or_404(Product, id=product_id)
        if product.seller and product.seller.type == 'seller': 
            product.is_approved = True
            product.save()
    return redirect('admin_dashboard')




@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.seller and not request.user.is_superuser:
        return redirect('product_list') 

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.category = request.POST.get('category')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')

        if request.FILES.get('image_front'):
            product.image_front = request.FILES.get('image_front')
        if request.FILES.get('image_back'):
            product.image_back = request.FILES.get('image_back')

        product.save()  

        return redirect('seller_dashboard')  

    return render(request, 'product_edit.html', {'product': product})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.seller and not request.user.is_superuser:
        return redirect('product_list') 

    if request.method == 'POST':
        product.delete() 
        return redirect('seller_dashboard') 

    return render(request, 'product_confirm_delete.html', {'product': product})

def products_by_category(request, category):
    query = request.GET.get('q', '').strip() 
    min_price = request.GET.get('min_price', 10)
    max_price = request.GET.get('max_price', 5000)
    sort_option = request.GET.get('orderby', 'menu_order')


    products = Product.objects.filter(
        is_active=True, 
        is_deleted=False
    ).filter(
        Q(is_approved=True) | Q(seller__is_superuser=True)
    )

    if category != 'all':
        products = products.filter(category=category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    products = products.filter(price__gte=min_price, price__lte=max_price)

    if sort_option == 'price':
        products = products.order_by('price')
    elif sort_option == 'price-desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('id')  

    paginator = Paginator(products, 6)  
    page_number = request.GET.get('page', 1)
    paginated_products = paginator.get_page(page_number)

    wishlist_count = 0
    cart_items = []
    wishlist_products = []
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).values_list('product_id', flat=True)
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        wishlist_products = Product.objects.filter(id__in=wishlist_items)
        wishlist_count = wishlist_items.count()

    return render(request, 'shop.html', {
        'products': paginated_products,
        'query': query, 
        'min_price': min_price,
        'max_price': max_price,
        'category': category or 'all',
        'orderby': sort_option,
        'cart_items': cart_items,
        'wishlist_products': wishlist_products,
        'wishlist_count': wishlist_count,
        'active_nav': 'products',
    })

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        user = CustomUser.objects.filter(email=email).first()

        if not user:
            return JsonResponse({'success': False, 'message': 'Email ID not registered.'})

        if CustomUser.objects.filter(email=email).count() > 1:
            return JsonResponse({'success': False, 'message': 'Multiple users found with this email. Please contact support.'})

        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail(
                'Reset Your Password',
                f'Click the link to reset your password: {reset_link}',
                'settings.EMAIL_HOST_USER',
                [email],
                fail_silently=False
            )
            return JsonResponse({'success': True, 'message': 'Password reset email sent successfully. Please check your inbox.'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Failed to send password reset email. Please try again later.'})

    return render(request, 'login-register.html')


def reset_password(request, token):
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    usr = CustomUser.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.set_password(new_password)
            password_reset.user.save()
            return redirect(login)
    return render(request, 'reset_password.html',{'token':token})

@login_required
def profile(request):
    user_type = "Admin" if request.user.is_superuser else "Seller"
    
    profile_data = {
        'last_login': request.user.last_login,
        'username': request.user.username,
        'email': request.user.email,
        'date_joined': request.user.date_joined,
        'user_type': user_type,
        'active_nav': 'profile',  
    }
    
    if request.user.is_superuser:
        return render(request, 'admindashboard.html', {**profile_data, 'user': request.user})
    else:
        return render(request, 'seller.html', {**profile_data, 'user': request.user})


def user_management(request):
    obj = CustomUser.objects.filter(type='user', is_staff=False, is_superuser=False)  
    sellers = CustomUser.objects.filter(type='seller')  

    if request.method == 'POST':
        seller_id = request.POST.get('seller_id')
        action = request.POST.get('action') 

        if action == 'approve':
            seller_profile = SellerProfile.objects.get(user__id=seller_id)
            seller_profile.is_approved = True
            seller_profile.save()
        elif action == 'reject':
            seller_profile = SellerProfile.objects.get(user__id=seller_id)
            seller_profile.is_approved = False
            seller_profile.save()

        return redirect('user_management') 

    return render(request, 'admindashboard.html', {'obj': obj, 'sellers': sellers, 'active_nav': 'users'})





def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('user_management')
    else:
        return render(request, 'user_edit.html', {'user': user})

def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_management')
    return render(request, 'confirm_delete_user.html', {'user': user})



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type', 'user')
        id_proof_type = request.POST.get('id_proof_type')
        id_proof_image = request.FILES.get('id_proof_image')

        if not username or not password or not email:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'login-register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'login-register.html')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e)
            return render(request, 'login-register.html')

        if user_type == 'seller':
            if not id_proof_type or not id_proof_image:
                messages.error(request, 'Please provide an ID proof type and image for seller registration.')
                return render(request, 'login-register.html')

        user = CustomUser.objects.create_user(username=username, password=password, email=email)
        user.type = user_type
        user.save()

        if user_type == 'seller':
            SellerProfile.objects.create(
                user=user,
                id_proof_type=id_proof_type,
                id_proof_image=id_proof_image, 
                is_approved=False 
            )
            messages.success(request, 'Registration successful. Please wait for admin approval as a seller.')
        else:
            messages.success(request, 'Registration successful. Welcome to the platform!')

        return redirect('login')
    
    return render(request, 'login-register.html')



def check_username(request):
    username = request.POST.get('username', None)
    exists = CustomUser.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            wishlist_count = Wishlist.objects.filter(user=user).count()

            
            if user.is_superuser:
                return redirect('admin')

            
            if user.type == 'seller':
                seller_profile = getattr(user, 'seller_profile', None)
                if seller_profile is not None and not seller_profile.is_approved:
                    messages.error(request, 'Your account is not approved by the admin.')
                    return render(request, 'login-register.html')
                return redirect('seller_dashboard')  
            
            return redirect('my-account')
            
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login-register.html')
    else:
        return render(request, 'login-register.html')


def logout(request):
    request.session.flush()
    return redirect('login')


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('seller_dashboard')

    products = Product.objects.all() 
    sellers = CustomUser.objects.filter(type='seller')  

    revenues = Revenue.objects.select_related('order_item__product', 'seller').all()

    total_seller_earnings = revenues.aggregate(Sum('seller_earning'))['seller_earning__sum'] or 0
    total_admin_earnings = revenues.aggregate(Sum('admin_earning'))['admin_earning__sum'] or 0

    context = {
        'products': products,
        'sellers': sellers,
        'revenues': revenues,
        'total_seller_earnings': total_seller_earnings,
        'total_admin_earnings': total_admin_earnings,
        'active_nav': 'products' 
    }

    return render(request, 'admindashboard.html', context)

@login_required
def admin_revenue_management(request):
    if not request.user.is_superuser:
        return redirect('seller_dashboard')  

    revenues = Revenue.objects.select_related('order_item__product', 'seller').all()
    total_seller_earnings = revenues.aggregate(Sum('seller_earning'))['seller_earning__sum'] or 0
    total_admin_earnings = revenues.aggregate(Sum('admin_earning'))['admin_earning__sum'] or 0
    context = {
        'revenues': revenues,
        'active_nav': 'earnings',  
        'total_seller_earnings': total_seller_earnings,
        'total_admin_earnings': total_admin_earnings,
    }

    return render(request, 'admindashboard.html', context)  

def seller_dashboard(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to access the seller dashboard.")
        return redirect('login')  

    if request.user.is_superuser:
        return redirect('admin_dashboard')

    if request.user.type != 'seller':
        request.session['show_seller_registration_error'] = True  

        return redirect('index') 

   
    products = Product.objects.filter(seller=request.user)

    orders = Order.objects.filter(order_items__product__seller=request.user,status='Pending' ).distinct()

    if request.method == 'POST':
        for order in orders:
            order_items = order.order_items.filter(product__seller=request.user)
            for item in order_items:
                item_status = request.POST.get(f'status_{item.id}')
                if item_status in ['pending', 'shipped', 'delivered', 'canceled']:
                    item.status = item_status
                    item.save()

        return redirect(f'seller_dashboard?tab=orders')

    orders_with_totals = []
    for order in orders:
        total_amount = 0
        order_items = order.order_items.filter(product__seller=request.user)
        order_item_details = []

        for item in order_items:
            total_amount += item.quantity * item.price
            order_item_details.append({
                'id': item.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.price,
                'status': item.status,
            })

        orders_with_totals.append({
            'order': order,
            'total_amount': total_amount,
            'order_items': order_item_details,
        })

    revenues = Revenue.objects.filter(seller=request.user).select_related('order_item__product')
    total_seller_earnings = sum(revenue.seller_earning for revenue in revenues)

    current_tab = request.GET.get('tab', 'products')

    return render(request, 'seller.html', {
        'products': products,
        'orders_with_totals': orders_with_totals,
        'revenues': revenues,
        'total_seller_earnings': total_seller_earnings,
        'active_nav': current_tab,
    })

def update_order_status(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        new_status = request.POST.get(f'status_{item_id}')
        item.status = new_status
        item.save()
    return redirect(f'/seller-dashboard/?tab=orders')



def index(request):
    wishlist_count = 0  
    show_seller_registration_error = request.session.pop('show_seller_registration_error', False)


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            wishlist_count = Wishlist.objects.filter(user=user).count()
            return render(request, 'index-2.html', {'wishlist_count': wishlist_count,
                'show_seller_registration_error': show_seller_registration_error})

    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(request, 'index-2.html', {'wishlist_count': wishlist_count,
                'show_seller_registration_error': show_seller_registration_error})


def contactus(request):
    wishlist_count = 0 

    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(request, 'contact-us.html', {'wishlist_count': wishlist_count})




def aboutus(r):
    return render(r,'about-us.html')



@login_required
def myaccount(request):
    user = request.user 

    address = None
    orders = Order.objects.filter(user=user, status='Pending').order_by('-order_date')  
    wishlist_count = Wishlist.objects.filter(user=user).count()

    if request.method == 'POST':
        new_username = request.POST.get('displayName')
        new_email = request.POST.get('email')
        new_password = request.POST.get('newPassword')

        if new_username and user.username != new_username:
            user.username = new_username

        if new_email and user.email != new_email:
            user.email = new_email

        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Account updated successfully!")

        return redirect(reverse('my-account') + '#account-details')

    else:
        try:
            address = Address.objects.get(user=user)
        except Address.DoesNotExist:
            address = None

    context = {
        'address': address,
        'orders': orders,  
        'wishlist_count': wishlist_count,  
    }
    return render(request, 'my-account.html', context)



@login_required
def fetch_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user, status='Pending').order_by('-order_date')

    return render(request, 'partials/orders_list.html', {'orders': orders})


@login_required
def save_address(request):
    if request.method == 'POST':
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            address = None

        if address:
            address.name = request.POST['name']
            address.phone = request.POST['phone']
            address.street = request.POST['street']
            address.apartment = request.POST['apartment']
            address.city = request.POST['city']
            address.postcode = request.POST['postcode']
            address.save()
            messages.success(request, "Your address has been updated successfully!")

        else:
            Address.objects.create(
                user=request.user,
                name=request.POST['name'],
                phone=request.POST['phone'],
                street=request.POST['street'],
                apartment=request.POST['apartment'],
                city=request.POST['city'],
                postcode=request.POST['postcode'],
            )
            messages.success(request, "Your address has been added successfully!")


        return redirect('/my-account#address')

    else:
        try:
            address = Address.objects.get(user=request.user)
        except Address.DoesNotExist:
            address = None

        context = {'address': address}
        return render(request, 'my_account.html', context)



import razorpay
import uuid

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if cart_items.exists():
        item_totals = [{
            'item': cart_item,
            'total_price': cart_item.quantity * cart_item.product.price
        } for cart_item in cart_items]
        total_amount = sum([i['total_price'] for i in item_totals])
    else:
        item_totals = None
        total_amount = 0

    try:
        saved_address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        saved_address = None
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    if request.method == 'POST':
        billing_name = request.POST.get('name')
        billing_phone = request.POST.get('phone')
        billing_street = request.POST.get('street')
        billing_apartment = request.POST.get('apartment', '')
        billing_city = request.POST.get('city')
        billing_postcode = request.POST.get('postcode')

        if not all([billing_name, billing_phone, billing_street, billing_city, billing_postcode]):
            return redirect('checkout')

        if not re.match(r'^\d{10}$', billing_phone):
            return redirect('checkout')

        valid_kerala_postcodes = re.compile(r'^(67[0-9]{4}|68[0-9]{4}|69[0-5][0-9]{3})$')
        if not valid_kerala_postcodes.match(billing_postcode):
            return redirect('checkout')

        if saved_address:
            saved_address.name = billing_name
            saved_address.phone = billing_phone
            saved_address.street = billing_street
            saved_address.apartment = billing_apartment
            saved_address.city = billing_city
            saved_address.postcode = billing_postcode
            saved_address.save()
        else:
            saved_address = Address.objects.create(
                user=request.user,
                name=billing_name,
                phone=billing_phone,
                street=billing_street,
                apartment=billing_apartment,
                city=billing_city,
                postcode=billing_postcode
            )

        with transaction.atomic(): 
            order = Order.objects.create(
                user=request.user,
                address=saved_address,
                total_amount=total_amount, 
                status='pending'  
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            request.session['payment_status_' + str(order.id)] = 'pending'

        request.session['shipping_address'] = {
            'name': billing_name,
            'street': billing_street,
            'apartment': billing_apartment,
            'city': billing_city,
            'postcode': billing_postcode
        }

        return redirect(reverse('payment', kwargs={'order_id': order.id}))  

    context = {
        'cart_items': cart_items,
        'item_totals': item_totals,
        'total_amount': total_amount,
        'saved_address': saved_address,
        'amount': int(total_amount * 100), 
        'wishlist_count': wishlist_count, 

    }

    return render(request, 'checkout.html', context)



import re

@login_required
def admin_order_management(request):
    orders = Order.objects.filter(status='Pending')  

    context = {
        'orders': orders,
        'active_nav': 'orders', 
    }
    
    return render(request, 'admindashboard.html', context)



@login_required
def delete_order(request, pk):
    if request.method == "POST":
        order = get_object_or_404(Order, pk=pk)
        order.delete()
    return redirect('admin_order_management')


@login_required
def admin_order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('order_items__product'), pk=pk)

    if request.method == 'POST':
        for item in order.order_items.all():
            item_status = request.POST.get(f'status_{item.id}')
            if item_status in ['pending', 'shipped', 'delivered', 'canceled']:
                if request.user.is_superuser and item.product.seller == request.user:
                    item.status = item_status
                    item.save()
                elif item.product.seller == request.user:
                    item.status = item_status
                    item.save()
        
        return redirect('admin_order_detail', pk=pk)

    order_items = order.order_items.all()

    context = {
        'order': order,
        'order_items': order_items,
        'is_admin': request.user.is_superuser,
        'current_user': request.user,
    }
    return render(request, 'order_detail.html', context)



@login_required
def order_details_view(request, order_id):
    try:
        order = Order.objects.prefetch_related('order_items__product').get(pk=order_id, user=request.user)
        shipping_address = order.address  
        expected_delivery_date = order.order_date + timedelta(days=5)


        order_items_with_totals = []
        for item in order.order_items.all():
            item_total = item.quantity * item.price 
            order_items_with_totals.append({
                'product': item.product,
                'quantity': item.quantity,
                'price': item.price,
                'total': item_total 
            })

        context = {
            'order': order,
            'order_items_with_totals': order_items_with_totals ,
            'shipping_address': shipping_address,
            'expected_delivery_date': expected_delivery_date 

        }
        return render(request, 'userorderdetail.html', context)
    except Order.DoesNotExist:
        return redirect('my_orders')




def send_low_stock_email(product):
    subject = f"Low Stock Alert: {product.name}"
    message = f"The stock for {product.name} is running low. Only {product.stock} left!"
    
    admin_email = settings.ADMIN_EMAIL 

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER, 
        [admin_email, product.seller.email],  
        fail_silently=False,
    )


@login_required
def payment(request, order_id):
    order = Order.objects.get(id=order_id)
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

    razorpay_order = client.order.create({
        'amount': int(order.total_amount * 100),  
        'currency': 'INR',
        'payment_capture': '1'
    })

    request.session['razorpay_order_id'] = razorpay_order['id']
    request.session['order_id'] = order.id 

    order.status = 'Payment Initiated'
    order.save()

    context = {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': 'rzp_test_SROSnyInFv81S4',
        'amount': order.total_amount, 
        'currency': 'INR'
    }

    return render(request, 'payment.html', context)

@login_required
def razorpay_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')

        session_razorpay_order_id = request.session.get('razorpay_order_id')
        order_id = request.session.get('order_id') 

        if razorpay_order_id == session_razorpay_order_id:
            try:
                order = Order.objects.prefetch_related('order_items__product').get(id=order_id)
            except Order.DoesNotExist:
                messages.error(request, "Order not found")
                return redirect('checkout')

            request.session['payment_status_' + str(order.id)] = 'paid'
            order.status = 'Pending' 
            order.save()

            for order_item in order.order_items.all():
                product = order_item.product
                
                if product.stock >= order_item.quantity:
                    product.stock -= order_item.quantity
                    product.save()

                    if product.stock <= 2:
                        send_low_stock_email(product)

                if not Revenue.objects.filter(order_item=order_item).exists():
                    price = Decimal(order_item.price)
                    quantity = Decimal(order_item.quantity)

                    seller_earning = price * quantity * Decimal('0.90')  
                    admin_earning = price * quantity * Decimal('0.10')  

                    Revenue.objects.create(
                        order_item=order_item,
                        seller=order_item.product.seller, 
                        seller_earning=seller_earning,
                        admin_earning=admin_earning
                    )

            CartItem.objects.filter(user=order.user).delete()

            if not request.session.get(f'email_sent_{order.id}', False):  
                subject = f"Order Confirmation - Order #{order.id}"
                message = f"""
                Dear {order.user.username},

                Thank you for your order! Your order has been successfully placed.

                Order Details:
                """

                for order_item in order.order_items.all():
                    message += f"\n {order_item.quantity} x {order_item.product.name} at ₹{order_item.price} each"

                message += f"\n\nTotal Amount: ₹{order.total_amount}\n\nWe hope you enjoy your purchase!"

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,  
                    [order.user.email],  
                    fail_silently=False,
                )

                request.session[f'email_sent_{order.id}'] = True

            expected_delivery_date = order.order_date + timedelta(days=5)

            return render(request, 'payment_success.html', {
                'order': order,
                'payment_id': payment_id,
                'expected_delivery_date': expected_delivery_date 
            })

    return redirect('checkout')


@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()

    customer_address = Address.objects.filter(user=order.user).first()
    if not customer_address:
        return HttpResponse("No address found for this order.", status=404)

    first_product = order_items[0].product
    seller = first_product.seller 
    seller_address = Address.objects.filter(user=seller).first()

    if not seller_address:
        return HttpResponse("No address found for the seller.", status=404)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(250, 750, "Invoice")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 720, "Order ID:")
    p.setFont("Helvetica", 12)
    p.drawString(150, 720, f"{order.id}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 705, "Order Date:")
    p.setFont("Helvetica", 12)
    p.drawString(150, 705, f"{order.order_date.strftime('%d-%m-%Y')}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 690, "Customer Name:")
    p.setFont("Helvetica", 12)
    p.drawString(150, 690, f"{customer_address.name}")

    p.line(45, 680, 565, 680)

    y_position = 650
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Shipping Address:")
    y_position -= 15
    p.setFont("Helvetica", 10)
    customer_address_lines = [
        f"{customer_address.phone}",
        f"{customer_address.street}",
        f"{customer_address.apartment}" if customer_address.apartment else None,
        f"{customer_address.city}, {customer_address.postcode}",
    ]
    for line in customer_address_lines:
        if line:
            p.drawString(60, y_position, line)
            y_position -= 15

    y_position -= 10
    p.line(45, y_position, 565, y_position)

    y_position -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Seller Details:")
    y_position -= 15
    p.setFont("Helvetica", 10)

    seller_details_lines = [
        f"Name: {seller_address.name}",
        f"Email: {seller.email}",
        f"Phone: {seller_address.phone}",
        f"Address: {seller_address.street}",
        f"{seller_address.apartment}" if seller_address.apartment else None,
        f"{seller_address.city}, {seller_address.postcode}",
    ]
    for line in seller_details_lines:
        if line:
            p.drawString(60, y_position, line)
            y_position -= 15

    y_position -= 20
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y_position, "Product Name")
    p.drawString(300, y_position, "Quantity")
    p.drawString(400, y_position, "Price")
    p.drawString(500, y_position, "Total")
    p.line(45, y_position - 5, 565, y_position - 5)
    y_position -= 15

    p.setFont("Helvetica", 10)
    for item in order_items:
        p.drawString(50, y_position, item.product.name)
        p.drawString(300, y_position, str(item.quantity))
        p.drawString(400, y_position, f"{item.price:.0f}")
        total_price = item.quantity * item.price
        p.drawString(500, y_position, f"{total_price:.0f}")
        y_position -= 15

        if y_position < 100:
            p.showPage()
            y_position = 750
            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, y_position, "Product Name")
            p.drawString(300, y_position, "Quantity")
            p.drawString(400, y_position, "Price")
            p.drawString(500, y_position, "Total")
            p.line(45, y_position - 5, 565, y_position - 5)
            y_position -= 15

    p.setFont("Helvetica-Bold", 12)
    p.drawString(400, y_position - 20, "Total Amount:")
    p.drawString(500, y_position - 20, f"Rs {order.total_amount:.0f}")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'
    return response
