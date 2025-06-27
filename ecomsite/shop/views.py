from django.shortcuts import render  ,redirect
from .models import Products , Orders
from django.core.paginator import Paginator
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




