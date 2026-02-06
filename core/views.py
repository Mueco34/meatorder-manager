from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from decimal import Decimal, InvalidOperation

from .models import Round, Customer, Product, Order, OrderItem


# Helper (KEIN login_required nötig)
def calc_travel_cost_eur(rnd):
    km_rate = getattr(settings, "KM_RATE", Decimal("0.30"))
    return (rnd.travel_km or Decimal("0")) * km_rate


@login_required
def home(request):
    active = Round.objects.filter(is_active=True).order_by("-date").first()
    return render(request, "core/home.html", {"active": active})


@login_required
def round_list(request):
    rounds = Round.objects.order_by("-is_active", "-date")
    return render(request, "core/round_list.html", {"rounds": rounds})


@login_required
def create_round(request):
    if request.method == "POST":
        date_str = request.POST.get("date")
        km_str = (request.POST.get("travel_km") or "0").replace(",", ".").strip()

        # Datum
        date = timezone.localdate() if not date_str else date_str  # YYYY-MM-DD

        # KM als Decimal speichern
        try:
            travel_km = Decimal(km_str)
        except (InvalidOperation, TypeError):
            travel_km = Decimal("0")

        rnd = Round.objects.create(date=date, travel_km=travel_km, is_active=True)
        Round.objects.exclude(id=rnd.id).update(is_active=False)

        return redirect("round_dashboard", round_id=rnd.id)

    return render(request, "core/create_round.html", {})


@login_required
def set_active_round(request, round_id):
    rnd = get_object_or_404(Round, id=round_id)
    Round.objects.update(is_active=False)
    rnd.is_active = True
    rnd.save()
    return redirect("round_dashboard", round_id=rnd.id)


@login_required
def shopping_list(request, round_id):
    rnd = get_object_or_404(Round, id=round_id)

    items = (
        OrderItem.objects
        .filter(order__round=rnd)
        .values("product__name", "product__unit")
        .annotate(total_qty=Sum("quantity"))
        .order_by("product__name")
    )

    return render(request, "core/shopping_list.html", {"round": rnd, "items": items})


@login_required
def pack_list(request, round_id):
    rnd = get_object_or_404(Round, id=round_id)

    orders = (
        Order.objects
        .filter(round=rnd)
        .select_related("customer")
        .prefetch_related("items__product")
        .order_by("customer__name")
    )

    return render(request, "core/pack_list.html", {"round": rnd, "orders": orders})


@login_required
def mark_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()
    return redirect("round_dashboard", round_id=order.round.id)


@login_required
def mark_picked(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.picked_up = True
    order.save()
    return redirect("round_dashboard", round_id=order.round.id)


@login_required
def round_profit(request, round_id):
    rnd = get_object_or_404(Round, id=round_id)

    totals = (
        OrderItem.objects
        .filter(order__round=rnd)
        .aggregate(
            revenue=Sum(ExpressionWrapper(F("sell_price") * F("quantity"), output_field=DecimalField())),
            cost=Sum(ExpressionWrapper(F("buy_price") * F("quantity"), output_field=DecimalField())),
        )
    )

    revenue = totals["revenue"] or Decimal("0")
    cost = totals["cost"] or Decimal("0")

    travel = calc_travel_cost_eur(rnd)
    profit = revenue - cost - travel

    return render(request, "core/round_profit.html", {
        "round": rnd,
        "revenue": revenue,
        "cost": cost,
        "travel": travel,
        "profit": profit,
        "km_rate": getattr(settings, "KM_RATE", Decimal("0.30")),
    })


@login_required
def round_dashboard(request, round_id):
    rnd = get_object_or_404(Round, id=round_id)

    shopping_items = (
        OrderItem.objects
        .filter(order__round=rnd)
        .values("product__name", "product__unit")
        .annotate(total_qty=Sum("quantity"))
        .order_by("product__name")
    )

    orders = (
        Order.objects
        .filter(round=rnd)
        .select_related("customer")
        .prefetch_related("items__product")
        .order_by("customer__name")
    )

    totals = (
        OrderItem.objects
        .filter(order__round=rnd)
        .aggregate(
            revenue=Sum(ExpressionWrapper(F("sell_price") * F("quantity"), output_field=DecimalField())),
            cost=Sum(ExpressionWrapper(F("buy_price") * F("quantity"), output_field=DecimalField())),
        )
    )

    revenue = totals["revenue"] or Decimal("0")
    cost = totals["cost"] or Decimal("0")

    travel = calc_travel_cost_eur(rnd)
    profit = revenue - cost - travel

    return render(request, "core/round_dashboard.html", {
        "round": rnd,
        "shopping_items": shopping_items,
        "orders": orders,
        "revenue": revenue,
        "cost": cost,
        "travel": travel,
        "profit": profit,
        "km_rate": getattr(settings, "KM_RATE", Decimal("0.30")),
    })


@login_required
def quick_order(request, round_id):
    rnd = get_object_or_404(Round, id=round_id)

    customers = Customer.objects.filter(active=True).order_by("name")
    products = Product.objects.filter(active=True).order_by("name")

    if request.method == "POST":
        customer_id = request.POST.get("customer")
        source = request.POST.get("source", "call")
        comment = request.POST.get("comment", "")

        if not customer_id:
            return HttpResponseBadRequest("Kunde fehlt")

        customer = get_object_or_404(Customer, id=customer_id)

        order = Order.objects.create(
            customer=customer,
            round=rnd,
            source=source,
            comment=comment,
        )

        created_items = 0
        for p in products:
            qty_str = (request.POST.get(f"qty_{p.id}") or "").strip().replace(",", ".")
            if not qty_str:
                continue
            try:
                qty = Decimal(qty_str)
            except (InvalidOperation, TypeError):
                continue
            if qty <= 0:
                continue

            OrderItem.objects.create(
                order=order,
                product=p,
                quantity=qty,
                sell_price=p.sell_price,
                buy_price=p.buy_price,
            )
            created_items += 1

        if created_items == 0:
            order.delete()
            return HttpResponseBadRequest("Keine Positionen eingegeben")

        return redirect("round_dashboard", round_id=rnd.id)

    return render(request, "core/quick_order.html", {
        "round": rnd,
        "customers": customers,
        "products": products,
    })


@login_required
def customer_list(request):
    q = (request.GET.get("q") or "").strip()
    customers = Customer.objects.all().order_by("name")
    if q:
        customers = customers.filter(Q(name__icontains=q) | Q(phone__icontains=q))
    return render(request, "core/customer_list.html", {"customers": customers, "q": q})


@login_required
def customer_create(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        active = request.POST.get("active") == "on"
        if name:
            Customer.objects.create(name=name, phone=phone, active=active)
            return redirect("customer_list")
    return render(request, "core/customer_form.html", {"title": "Neuer Kunde", "customer": None})


@login_required
def customer_edit(request, customer_id):
    c = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        c.name = (request.POST.get("name") or "").strip()
        c.phone = (request.POST.get("phone") or "").strip()
        c.active = request.POST.get("active") == "on"
        c.save()
        return redirect("customer_list")
    return render(request, "core/customer_form.html", {"title": "Kunde bearbeiten", "customer": c})


@login_required
def product_list(request):
    q = (request.GET.get("q") or "").strip()
    products = Product.objects.all().order_by("name")
    if q:
        products = products.filter(Q(name__icontains=q) | Q(unit__icontains=q))
    return render(request, "core/product_list.html", {"products": products, "q": q})


@login_required
def product_create(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        unit = (request.POST.get("unit") or "").strip() or "kg"
        buy_price = (request.POST.get("buy_price") or "0").replace(",", ".").strip()
        sell_price = (request.POST.get("sell_price") or "0").replace(",", ".").strip()
        active = request.POST.get("active") == "on"

        if name:
            try:
                buy_price_val = Decimal(buy_price)
            except (InvalidOperation, TypeError):
                buy_price_val = Decimal("0")
            try:
                sell_price_val = Decimal(sell_price)
            except (InvalidOperation, TypeError):
                sell_price_val = Decimal("0")

            Product.objects.create(
                name=name,
                unit=unit,
                buy_price=buy_price_val,
                sell_price=sell_price_val,
                active=active,
            )
            return redirect("product_list")

    return render(request, "core/product_form.html", {"title": "Neues Produkt", "product": None})


@login_required
def product_edit(request, product_id):
    p = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        p.name = (request.POST.get("name") or "").strip()
        p.unit = (request.POST.get("unit") or "").strip() or "kg"

        buy_price = (request.POST.get("buy_price") or "0").replace(",", ".").strip()
        sell_price = (request.POST.get("sell_price") or "0").replace(",", ".").strip()

        try:
            p.buy_price = Decimal(buy_price)
        except (InvalidOperation, TypeError):
            p.buy_price = Decimal("0")

        try:
            p.sell_price = Decimal(sell_price)
        except (InvalidOperation, TypeError):
            p.sell_price = Decimal("0")

        p.active = request.POST.get("active") == "on"
        p.save()
        return redirect("product_list")

    return render(request, "core/product_form.html", {"title": "Produkt bearbeiten", "product": p})


@login_required
def order_edit(request, order_id):
    order = get_object_or_404(Order.objects.select_related("round", "customer"), id=order_id)
    rnd = order.round
    products = Product.objects.all().order_by("name")
    existing_items = {item.product_id: item for item in order.items.select_related("product").all()}

    if request.method == "POST":
        order.comment = (request.POST.get("comment") or "").strip()
        order.source = request.POST.get("source") or order.source
        order.save()

        for p in products:
            qty_str = (request.POST.get(f"qty_{p.id}") or "").strip().replace(",", ".")
            try:
                qty = Decimal(qty_str) if qty_str != "" else Decimal("0")
            except (InvalidOperation, TypeError):
                qty = Decimal("0")

            item = existing_items.get(p.id)

            if qty <= 0:
                if item:
                    item.delete()
                continue

            if item:
                item.quantity = qty
                item.save()
            else:
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    quantity=qty,
                    sell_price=p.sell_price,
                    buy_price=p.buy_price,
                )

        if not order.items.exists():
            order.delete()

        return redirect("round_dashboard", round_id=rnd.id)

    qty_map = {pid: existing_items[pid].quantity for pid in existing_items}
    return render(request, "core/order_edit.html", {
        "order": order,
        "round": rnd,
        "products": products,
        "qty_map": qty_map,
    })


@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    rnd_id = order.round_id
    if request.method == "POST":
        order.delete()
    return redirect("round_dashboard", round_id=rnd_id)


@login_required
def round_mark_all_paid(request, round_id):
    rnd = get_object_or_404(Round, id=round_id)
    if request.method == "POST":
        Order.objects.filter(round=rnd).update(paid=True)
    return redirect("round_dashboard", round_id=rnd.id)


@login_required
def round_mark_all_picked(request, round_id):
    rnd = get_object_or_404(Round, id=round_id)
    if request.method == "POST":
        Order.objects.filter(round=rnd).update(picked_up=True)
    return redirect("round_dashboard", round_id=rnd.id)
