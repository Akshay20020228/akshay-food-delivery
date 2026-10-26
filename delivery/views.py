

from django.shortcuts import render, redirect
from .models import FoodItem, Order


def home(request):
    foods = FoodItem.objects.filter(available=True)
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    return render(request, "delivery/home.html", {
        "foods": foods,
        "cart_count": cart_count,
    })


def add_to_cart(request, food_id):
    if request.method == "POST":
        food = FoodItem.objects.get(
            id=food_id,
            available=True
        )

        cart = request.session.get("cart", {})
        key = str(food.id)
        cart[key] = cart.get(key, 0) + 1

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("home")


def view_cart(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0

    for food_id, quantity in cart.items():
        try:
            food = FoodItem.objects.get(
                id=int(food_id),
                available=True
            )

            subtotal = food.price * quantity
            total += subtotal

            items.append({
                "food": food,
                "quantity": quantity,
                "subtotal": subtotal,
            })

        except FoodItem.DoesNotExist:
            continue

    return render(request, "delivery/cart.html", {
        "items": items,
        "total": total,
    })



def checkout(request):
    cart = request.session.get("cart", {})
    total = 0

    for food_id, quantity in cart.items():
        try:
            food = FoodItem.objects.get(id=int(food_id), available=True)
            total += food.price * quantity
        except FoodItem.DoesNotExist:
            continue

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if not cart:
            return redirect("view_cart")

        if not customer_name or not phone or not address:
            return render(request, "delivery/checkout.html", {
                "total": total,
                "error": "Please fill in all the details.",
            })

        if total <= 0:
            return redirect("view_cart")

        Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            address=address,
            total_amount=total,
        )

        request.session["cart"] = {}
        return redirect("order_success")

    return render(request, "delivery/checkout.html", {"total": total})


def order_success(request):
    return render(request, "delivery/order_success.html")


def view_orders(request):
    orders = Order.objects.all().order_by("-created_at")

    return render(request, "delivery/view_orders.html", {
        "orders": orders
    })


def update_order_status(request, order_id):
    if request.method == "POST":
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")

        valid_statuses = [
            choice[0] for choice in Order.STATUS_CHOICES
        ]

        if new_status in valid_statuses:
            order.status = new_status
            order.save()

    return redirect("view_orders")

