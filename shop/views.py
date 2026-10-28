from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CheckoutForm
from .models import SIZES, Category, Order, OrderItem, Product


def bag_lines(request):
    cart = request.session.get("cart", {})
    products = Product.objects.in_bulk({int(k.split(":")[0]) for k in cart})
    lines, subtotal = [], Decimal(0)
    for key, qty in cart.items():
        pid, size = key.split(":")
        p = products.get(int(pid))
        if p:
            lines.append({"key": key, "product": p, "size": size, "qty": qty, "subtotal": p.price * qty})
            subtotal += p.price * qty
    shipping = Decimal(0) if (subtotal >= settings.FREE_SHIPPING_ABOVE or not lines) else Decimal(settings.SHIPPING_FEE)
    return lines, subtotal, shipping


def home(request):
    return render(request, "shop/home.html", {
        "featured": Product.objects.filter(featured=True)[:4],
        "categories": Category.objects.all(),
    })


def shop(request):
    items = Product.objects.select_related("category")
    cat = request.GET.get("cat", "")
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "new")
    if cat: items = items.filter(category__slug=cat)
    if q: items = items.filter(Q(name__icontains=q) | Q(description__icontains=q))
    items = items.order_by({"low": "price", "high": "-price"}.get(sort, "-created"))
    return render(request, "shop/shop.html", {
        "products": items, "categories": Category.objects.all(), "cat": cat, "q": q, "sort": sort,
    })


def product(request, slug):
    p = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=p.category).exclude(pk=p.pk)[:4]
    return render(request, "shop/product.html", {"p": p, "sizes": SIZES, "related": related})


def bag(request):
    lines, subtotal, shipping = bag_lines(request)
    return render(request, "shop/bag.html", {"lines": lines, "subtotal": subtotal, "shipping": shipping, "total": subtotal + shipping})


@require_POST
def bag_add(request):
    ajax = request.headers.get("X-Requested-With") == "fetch"
    p = get_object_or_404(Product, pk=request.POST.get("product"))
    size = request.POST.get("size", "")
    try:
        qty = max(1, min(int(request.POST.get("qty", 1)), 10))
    except ValueError:
        qty = 1
    cart = request.session.get("cart", {})
    key = f"{p.pk}:{size}"
    if size not in SIZES or p.stock < cart.get(key, 0) + qty:
        err = "Pick a size." if size not in SIZES else f"Only {p.stock} left in stock."
        return JsonResponse({"ok": False, "error": err}) if ajax else redirect("product", slug=p.slug)
    cart[key] = cart.get(key, 0) + qty
    request.session["cart"] = cart
    if ajax:
        return JsonResponse({"ok": True, "count": sum(cart.values())})
    return redirect("bag")


@require_POST
def bag_update(request):
    cart = request.session.get("cart", {})
    key = request.POST.get("key", "")
    if key in cart:
        try:
            qty = int(request.POST.get("qty", 0))
        except ValueError:
            qty = 0
        if qty <= 0: cart.pop(key)
        else: cart[key] = min(qty, 10)
        request.session["cart"] = cart
    return redirect("bag")


def checkout(request):
    lines, subtotal, shipping = bag_lines(request)
    if not lines:
        return redirect("bag")
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.shipping, order.total = shipping, subtotal + shipping
            order.save()
            for l in lines:
                p = Product.objects.select_for_update().get(pk=l["product"].pk)
                if p.stock < l["qty"]:
                    transaction.set_rollback(True)
                    form.add_error(None, f"{p.name} just sold out in that quantity. Update your bag.")
                    break
                p.stock -= l["qty"]; p.save(update_fields=["stock"])
                OrderItem.objects.create(order=order, product=p, name=p.name, size=l["size"], price=p.price, qty=l["qty"])
            else:
                request.session["cart"] = {}
                request.session["last_order"] = order.pk
                return redirect("order_done", pk=order.pk)
    return render(request, "shop/checkout.html", {"form": form, "lines": lines, "subtotal": subtotal, "shipping": shipping, "total": subtotal + shipping})


def order_done(request, pk):
    if request.session.get("last_order") != pk:
        return redirect("home")
    return render(request, "shop/done.html", {"order": get_object_or_404(Order, pk=pk)})
