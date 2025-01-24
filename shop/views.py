from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from itertools import islice
from django.contrib import messages

import json
from django.views.decorators.csrf import csrf_exempt
from profiles import models
from profiles.models import UserExtra
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
import datetime

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
    

    return render(request, 'shop/cart.html')



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



razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
@login_required(login_url='/profile/login')
def checkout(request):
    print(request.user)
    user_obj = models.UserExtra.objects.get(user = request.user)

    if request.method == "POST":
        
        try:
            # Extract necessary details from the JSON
            items_json = request.POST.get('items_json','')
            name = request.POST.get('name','')
            amount = request.POST.get('total_price','')
            email = request.POST.get('email','')
            address = request.POST.get('address','')
            phone = request.POST.get('phone','')
            city = request.POST.get('city','')
            state = request.POST.get('state','')
            zip_code = request.POST.get('zip_code','')

            # Print inputs for debugging
            print(f"Received: {items_json}, {name}, {email}, {address}, {phone}, {city}, {state}, {zip_code}, {amount}")

            # Process payment with Razorpay
            currency = 'INR'
            razorpay_amount = int(amount) * 100  # Convert to paise
            
            razorpay_order = razorpay_client.order.create({
                'amount': razorpay_amount,
                'currency': currency,
                'payment_capture': '0'
            })
            
            print("*****")
            print("Razorpay Order:", razorpay_order)
            print("*****")
            
            order = Orders.objects.create(
                user=request.user,
                items_json=items_json,
                name=name,
                email=email,
                address=address,
                phone=phone,
                city=city,
                state=state,
                zip_code=zip_code,
                amount=amount,
                razorpay_order_id=razorpay_order['id'],
                currency = currency,
                status = 'PENDING'
            )
            
            order_update = OrderUpdate.objects.create(
                order_id = order,
                update_desc = "Your order is placed"
                
            )
            order_update.save()

            # Save user extra details (not order yet)
            user_obj.pincode = zip_code
            user_obj.email = email
            user_obj.name = name
            user_obj.city = city
            user_obj.state = state
            user_obj.phone_number = phone
            user_obj.address = address
            user_obj.save()

            

            # Prepare context for payment page
            context = {
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_merchant_key': settings.RAZOR_KEY_ID,
                'razorpay_amount': razorpay_amount,
                'currency': currency,
                'name': name,
                'email': email,
                'phone': phone,
                'address': address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'callback_url' : 'handler/'
            }
            print("*****")
            print("context:" , context)
            print("*****")

            return render(request, 'shop/payment.html', context)

        except Exception as e:
            print(f"Error processing payment: {e}")
            # return JsonResponse({"status": "error", "message": "Something went wrong. Please try again."})

    # GET request
    return render(request, 'shop/checkout.html', {'user_obj':user_obj})


def payment(request):
    
    return render(request , 'shop/payment.html',{})

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        try:
            # Get payment details from Razorpay
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')

            # Verify payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            print(params_dict)
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Update order status
            order = Orders.objects.get(razorpay_order_id=razorpay_order_id)
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.status = 'SUCCESS'
            order.save()

            return render(request, 'shop/thankyou.html',{"order":order})

        except Orders.DoesNotExist:
            print("Order not found")
            return HttpResponse("Order not found", status=400)
        except razorpay.errors.SignatureVerificationError:
            return HttpResponse("Invalid payment signature", status=400)
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("Payment verification failed", status=500)

    return HttpResponse("Invalid request method", status=405)
                
@login_required(login_url='/profile/login')
def settings(request):
    try:
        user_extra = UserExtra.objects.get(user=request.user)
        user=request.user
    except UserExtra.DoesNotExist:
        messages.error(request, "UserExtra details not found.")
        return render(request, 'shop/profile_settings.html')
    except User.DoesNotExist:
        messages.error(request, "User details not found.")
        return render(request, 'shop/profile_settings.html')
    if request.method == 'POST':
        try:
            
            user.username = request.POST.get('username','')
            user.first_name = request.POST.get('first_name','') 
            user.last_name =  request.POST.get('last_name','')
            user.email = request.POST.get('email','') 
            user.save()  
            user_extra.phone_number = request.POST.get('number','')
            user_extra.bio = request.POST.get('bio','')
            user_extra.address = request.POST.get('location','')
            user_extra.state = request.POST.get('state','')
            user_extra.city = request.POST.get('city','')
            user_extra.pincode = request.POST.get('pincode','')
            user_extra.birth_date =  request.POST.get('birth_date','')
            profile_picture = request.FILES.get('profile_picture','')
            if profile_picture:
                user_extra.profile_picture = profile_picture
            
            user_extra.save()            
            messages.success(request,'update successfully')
        except Exception as e:
            print("user_extra could not be saved",e)
        
    return render(request, 'shop/profile_settings.html')
        