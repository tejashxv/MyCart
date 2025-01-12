from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from itertools import groupby
from itertools import islice
import json

from math import ceil
# Create your views here.
from itertools import islice

def index(request): 
    products = Products.objects.all()
    categories = Products.objects.values('category').distinct()
    allprod = []

    def chunk_products(products, chunk_size):
        """Helper function to divide products into chunks of specified size."""
        products = iter(products)
        return iter(lambda: list(islice(products, chunk_size)), [])

    for category in categories:
        category_name = category['category']
        category_products = Products.objects.filter(category=category_name)
        product_chunks = list(chunk_products(category_products, 4))  # Divide products into groups of 4
        allprod.append({
            'category': category_name,
            'product_chunks': product_chunks
        })

    params = {'allprod': allprod}
    return render(request, 'shop/index.html', params)


def cart(request):
    products = Products.objects.all()  # or any logic to get the products

    return render(request, 'shop/cart.html', {'products': products})



def about(request):
    return render(request, "shop/about.html")
    
def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        
    return render(request, "shop/contact.html", {'thank':thank})

    
def tracker(request):
    
    if request.method == "POST":
        orderid = request.POST.get('orderid', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.get(order_id=orderid, email=email)
            orderupdate = OrderUpdate.objects.filter(order_id=order)
            print(orderupdate)
            print(order)
            
            return render(request, "shop/tracker.html", {'product': order, 'orderupdate': orderupdate})
            
            # if len(order) > 0:
            #     update = OrderUpdate.objects.filter(order_id=orderid)
            #     updates = []
            #     for item in update:
            #         updates.append({'text': item.update_desc, 'time': item.timestamp})
            #         response = json.dumps(updates, default=str)
            #         print(updates)
            #     return render(request, "shop/tracker.html", {'updates': updates, 'order': order[0]})
            # else:
            #     pass
        except Exception as e: 
            pass
    return render(request, "shop/tracker.html")

    
def search(request):
    return HttpResponse("this is search")
def Thankyou(request):
    try:
        id = Orders.objects.latest('order_id')
    except id.DoesNotExist as e:
        print(f"Error getting order ID: {e}")
        
    if id:
        return render(request, "shop/thankyou.html",{'id':id})
    else:
        return render(request, "shop/thankyou.html")
    
    
def productview(request, myid):
    products = Products.objects.filter(id=myid)
    print(products)
    return render(request, "shop/prodview.html" , {'products':products[0]})
    
    
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')

        # Print inputs for debugging
        print(f"Received: {items_json}, {name}, {email}, {address}, {phone}, {city}, {state}, {zip_code}")

        # Save the order
        try:
            orders = Orders(
                items_json=items_json,
                name=name,
                email=email,
                address=address,
                phone=phone,
                city=city,
                state=state,
                zip_code=zip_code
            )
            orders.save()

            print(f"Order saved with ID: {orders.order_id}")

            placed = True
            
            update = OrderUpdate(order_id=orders, update_desc=f"The order {orders.order_id} has been placed.")
            update.save()
            return render(request, 'shop/thankyou.html', {'placed': placed, 'id': orders.order_id})
        except Exception as e:
            # Print errors
            print(f"Error saving order: {e}")
            return render(request, 'shop/checkout.html', {'error': 'Order could not be saved.'})

    return render(request, 'shop/checkout.html')

    
    
    