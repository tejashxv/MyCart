from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from itertools import groupby
from itertools import islice

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
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        
    return render(request, "shop/contact.html")

    
def tracker(request):
    return render(request, "shop/tracker.html")

    
def search(request):
    return HttpResponse("this is search")
    
    
def productview(request, myid):
    products = Products.objects.filter(id=myid)
    print(products)
    return render(request, "shop/prodview.html" , {'products':products[0]})
    
    
def checkout(request):
    products = Products.objects.all()  # or any logic to get the products

    return render(request, 'shop/checkout.html', {'products': products})
    
    
    