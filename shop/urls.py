from django.contrib import admin
from django.urls import path
from .  import views,models


urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("cart/",views.cart,name="About"),
    path("about/",views.about,name="About"),
    path("contact/",views.contact,name="Contact"),
    path("tracker/",views.tracker,name="Tracker"),
    path("search/",views.search,name="Search"),
    path("productview/<int:myid>",views.productview,name="ProductView"),
    path("checkout/",views.checkout,name="Checkout"),
    path("order/",views.Thankyou,name="Thankyou"),
    path("payment/",views.payment,name="payment"),
    path("handler/",views.verify_payment,name="paymenthandler"),
    path("profile-settings/",views.settingss,name="settingss"),
    
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    # path("handlerequest/",views.handlerequest,name="handleRequest"),
]
