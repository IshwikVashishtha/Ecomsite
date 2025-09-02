from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import razorpay
from decimal import Decimal

from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review
from .forms import UserRegistrationForm, CheckoutForm, ReviewForm, SearchForm

# Razorpay configuration
razorpay_client = razorpay.Client(
    auth=("rzp_test_YOUR_KEY_ID", "YOUR_SECRET_KEY")
)

def index(request):
    """Home page with product listing and search functionality"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Search and filter functionality
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category_id = search_form.cleaned_data.get('category')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        sort_by = search_form.cleaned_data.get('sort_by')
        
        if query:
            products = products.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        
        if category_id:
            products = products.filter(category_id=category_id)
        
        if min_price:
            products = products.filter(final_price__gte=min_price)
        
        if max_price:
            products = products.filter(final_price__lte=max_price)
        
        # Sorting
        if sort_by == 'price_low':
            products = products.order_by('discount_price', 'price')
        elif sort_by == 'price_high':
            products = products.order_by('-discount_price', '-price')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        elif sort_by == 'rating':
            products = products.order_by('-rating')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
        'search_form': search_form,
    }
    return render(request, 'shop/index.html', context)

def product_detail(request, product_id):
    """Product detail page with reviews and similar products"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    similar_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    reviews = product.reviews.all()
    review_form = ReviewForm()
    
    context = {
        'product': product,
        'similar_products': similar_products,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'shop/product_detail.html', context)

@login_required
def add_review(request, product_id):
    """Add a review for a product"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Review added successfully!')
        else:
            messages.error(request, 'Error adding review.')
    
    return redirect('product_detail', product_id=product_id)

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'shop/login.html')

@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('index')

@login_required
def cart_view(request):
    """Shopping cart view"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'shop/cart.html', context)

@login_required
@require_POST
def add_to_cart(request):
    """Add product to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart!',
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def update_cart_item(request):
    """Update cart item quantity"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        if quantity <= 0:
            cart_item.delete()
            message = 'Item removed from cart!'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Cart updated!'
        
        cart = cart_item.cart
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price),
            'item_total': float(cart_item.total_price)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart!',
            'cart_count': cart.total_items,
            'cart_total': float(cart.total_price)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

@login_required
def checkout(request):
    """Checkout page"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode'],
                subtotal=cart.total_price,
                total_amount=cart.total_price
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.final_price,
                    total_price=cart_item.total_price
                )
            
            # Clear cart
            cart.delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('order_detail', order_id=order.order_id)
    else:
        form = CheckoutForm()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'form': form,
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def create_razorpay_order(request):
    """Create Razorpay order for payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            order = get_object_or_404(Order, order_id=order_id, user=request.user)
            
            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                'amount': int(order.total_amount * 100),  # Amount in paisa
                'currency': 'INR',
                'receipt': str(order.order_id),
                'payment_capture': 1
            })
            
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            
            return JsonResponse({
                'success': True,
                'order_id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency']
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=405)

@csrf_exempt
def verify_payment(request):
    """Verify Razorpay payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')
            
            # Verify payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Update order status
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.payment_status = 'paid'
            order.razorpay_payment_id = razorpay_payment_id
            order.status = 'confirmed'
            order.save()
            
            return JsonResponse({'success': True, 'message': 'Payment verified successfully!'})
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=405)

@login_required
def order_list(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'shop/order_list.html', context)

@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    context = {
        'order': order
    }
    return render(request, 'shop/order_detail.html', context)

def category_products(request, category_slug):
    """Products filtered by category"""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category_products.html', context)

