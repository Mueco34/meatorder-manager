"""
URL configuration for meatmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # STARTSEITE
    path("", views.home, name="home"),

    # Runden
    path("runden/", views.round_list, name="round_list"),
    path("runde/<int:round_id>/", views.round_dashboard, name="round_dashboard"),
    path("runde/neu/", views.create_round, name="create_round"),
    path("runde/<int:round_id>/aktiv/", views.set_active_round, name="set_active_round"),
    path("runde/<int:round_id>/gewinn/", views.round_profit, name="round_profit"),

    # Listen
    path("runden/<int:round_id>/einkaufsliste/", views.shopping_list, name="shopping_list"),
    path("runden/<int:round_id>/packliste/", views.pack_list, name="pack_list"),

    # Bestellungen
    path("runde/<int:round_id>/bestellung/neu/", views.quick_order, name="quick_order"),
    path("order/<int:order_id>/paid/", views.mark_paid, name="mark_paid"),
    path("order/<int:order_id>/picked/", views.mark_picked, name="mark_picked"),
    path("order/<int:order_id>/edit/", views.order_edit, name="order_edit"),
    path("order/<int:order_id>/delete/", views.order_delete, name="order_delete"),

    # Schnellaktionen
    path("runde/<int:round_id>/alle-bezahlt/", views.round_mark_all_paid, name="round_mark_all_paid"),
    path("runde/<int:round_id>/alle-abgeholt/", views.round_mark_all_picked, name="round_mark_all_picked"),

    # Kunden / Produkte
    path("kunden/", views.customer_list, name="customer_list"),
    path("kunden/neu/", views.customer_create, name="customer_create"),
    path("kunden/<int:customer_id>/edit/", views.customer_edit, name="customer_edit"),

    path("produkte/", views.product_list, name="product_list"),
    path("produkte/neu/", views.product_create, name="product_create"),
    path("produkte/<int:product_id>/edit/", views.product_edit, name="product_edit"),
]
