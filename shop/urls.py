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
    path("order/",views.Thankyou,name="Checkout"),
    path("handlerequest/",views.handlerequest,name="handleRequest"),
]
