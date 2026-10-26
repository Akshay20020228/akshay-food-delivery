
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-to-cart/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/", views.order_success, name="order_success"),
    path("orders/", views.view_orders, name="view_orders"),
    path(
    "orders/<int:order_id>/update/",
    views.update_order_status,
    name="update_order_status",
),
]
