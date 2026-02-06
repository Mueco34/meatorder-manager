from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("runden/", views.round_list, name="round_list"),
    path("runden/<int:round_id>/einkaufsliste/", views.shopping_list, name="shopping_list"),
    path("runden/<int:round_id>/packliste/", views.pack_list, name="pack_list"),
    path("order/<int:order_id>/paid/", views.mark_paid, name="mark_paid"),
    path("order/<int:order_id>/picked/", views.mark_picked, name="mark_picked"),
    path("runden/<int:round_id>/gewinn/", views.round_profit, name="round_profit"),
    path("runden/<int:round_id>/dashboard/", views.round_dashboard, name="round_dashboard"),
    path("runden/<int:round_id>/neu/", views.quick_order, name="quick_order"),
    path("runden/<int:round_id>/aktiv/", views.set_active_round, name="set_active_round"),
    path("runden/neu/", views.create_round, name="create_round"),
    path("kunden/", views.customer_list, name="customer_list"),
    path("kunden/neu/", views.customer_create, name="customer_create"),
    path("kunden/<int:customer_id>/bearbeiten/", views.customer_edit, name="customer_edit"),
    path("produkte/", views.product_list, name="product_list"),
    path("produkte/neu/", views.product_create, name="product_create"),
    path("produkte/<int:product_id>/bearbeiten/", views.product_edit, name="product_edit"),
    path("order/<int:order_id>/bearbeiten/", views.order_edit, name="order_edit"),
    path("order/<int:order_id>/loeschen/", views.order_delete, name="order_delete"),
    path("runden/<int:round_id>/alle-bezahlt/", views.round_mark_all_paid, name="round_mark_all_paid"),
    path("runden/<int:round_id>/alle-abgeholt/", views.round_mark_all_picked, name="round_mark_all_picked"),


]
