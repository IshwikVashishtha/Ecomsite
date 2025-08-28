from django.shortcuts import render  ,redirect
from .models import Products , Orders
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .razorpay_client import razorpay_client
import json
# Create your views here.


def index(request):
    product_objects =Products.objects.all()

    item_name = request.GET.get("item_name")
    if item_name != "" and item_name is not None:
        product_objects = product_objects.filter(title__icontains= item_name)

    paginator =Paginator(product_objects , 3)
    page = request.GET.get('page')
    product_objects =paginator.get_page(page)
    return render(request , 'shop/index.html' ,{'product_objects':product_objects}) 



  
def details(request , id ):
    product_object = Products.objects.get(id = id)
    similar_products = Products.objects.filter(category=product_object.category).exclude(id=product_object.id)[:4]

    return render(request , 'shop/detail.html' , {'product_object': product_object , 'similar_products': similar_products})


def checkout(request):

    if request.method == 'POST':
        # print("POST data:", request.POST)  # Debug: See all submitted data
        name = request.POST.get('inputName')
        email = request.POST.get('inputEmail4')
        password = request.POST.get('inputPassword4')
        address = request.POST.get('inputAddress')
        city = request.POST.get('inputCity')
        state = request.POST.get('inputState')
        zipcode = request.POST.get('inputZip')
        totalprice = float(request.POST.get('total'))
        items = request.POST.get('items')
        order = Orders( name =name ,
                            email = email,
                            password =password,
                            address =address,
                            city =city,
                            state =state,
                            zipcode =zipcode,
                            Items = items, 
                            totalprice = totalprice, )
        order.save()
        return redirect('/')
    return render (request , 'shop/checkout.html')

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .razorpay_client import razorpay_client
import json

def create_razorpay_order(request):
    if request.method == 'POST':
        # Get data from the frontend
        data = json.loads(request.body)
        total_amount = int(float(data.get('total')) * 100)  # Amount in paisa
        
        # Create a Razorpay order on the server
        order_receipt = 'order_' + str(total_amount)
        order_data = {
            'amount': total_amount,  # Amount in paisa
            'currency': 'INR',
            'receipt': order_receipt,
            'payment_capture': 1
        }
        try:
            razorpay_order = razorpay_client.order.create(data=order_data)
            return JsonResponse({'order_id': razorpay_order['id'], 'amount': total_amount})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            payment_data = json.loads(data)
            
            razorpay_order_id = payment_data.get('razorpay_order_id')
            razorpay_payment_id = payment_data.get('razorpay_payment_id')
            razorpay_signature = payment_data.get('razorpay_signature')
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            # Verify the payment signature. This is a critical security step.
            razorpay_client.utility.verify_payment_signature(params_dict)

            # If the signature is valid, process the order
            # e.g., save the order details to your database, clear the cart, etc.
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

