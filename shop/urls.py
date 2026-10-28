from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("product/<slug:slug>/", views.product, name="product"),
    path("bag/", views.bag, name="bag"),
    path("bag/add/", views.bag_add, name="bag_add"),
    path("bag/update/", views.bag_update, name="bag_update"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:pk>/", views.order_done, name="order_done"),
]
