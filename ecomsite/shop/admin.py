from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'discount_price', 'stock', 'is_active', 'rating', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'category__name']
    list_editable = ['price', 'discount_price', 'stock', 'is_active']
    ordering = ['-created_at']

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]
    readonly_fields = ['total_items', 'total_price']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'name', 'status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_id', 'user__username', 'name', 'email']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'user', 'status', 'payment_status', 'created_at', 'updated_at')
        }),
        ('Customer Information', {
            'fields': ('name', 'email', 'phone', 'address', 'city', 'state', 'zipcode')
        }),
        ('Order Details', {
            'fields': ('subtotal', 'tax', 'shipping', 'total_amount')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'razorpay_order_id', 'razorpay_payment_id')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'product__title', 'comment']
    readonly_fields = ['created_at']
    ordering = ['-created_at']