from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40, blank=True)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120)
    unit = models.CharField(max_length=20, default="kg")
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Round(models.Model):
    date = models.DateField()
    is_active = models.BooleanField(default=False)

    # statt travel_cost (Euro) speichern wir jetzt km
    travel_km = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Round {self.date}"


class Order(models.Model):
    class Source(models.TextChoices):
        CALL = "call", "Anruf"
        WHATSAPP = "whatsapp", "WhatsApp"
        SELF = "self", "Kunde selbst"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.CALL)
    comment = models.TextField(blank=True)
    paid = models.BooleanField(default=False)
    picked_up = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} – {self.round}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)

    sell_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # nur beim ersten Speichern
            self.sell_price = self.product.sell_price
            self.buy_price = self.product.buy_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} ({self.quantity} {self.product.unit})"
