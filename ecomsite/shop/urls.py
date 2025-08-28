from django.urls import path
from . import views

urlpatterns = [
    path('create-razorpay-order/', views.create_razorpay_order, name='create-razorpay-order'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
]