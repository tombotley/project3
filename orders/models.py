from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

import datetime

# Create your models here.


class Pizza(models.Model):
    desc = models.CharField(max_length = 20)

    def __str__(self):
        return self.desc


class Topping(models.Model):
    desc = models.CharField(max_length = 20)

    def __str__(self):
        return self.desc


class Style(models.Model):
    desc = models.CharField(max_length = 20)

    def __str__(self):
        return self.desc


class Size(models.Model):
    desc = models.CharField(max_length = 20)

    def __str__(self):
        return self.desc


class PizzaPrice(models.Model):
    pizza_type = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="pizza_type")
    pizza_style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name="pizza_style")
    pizza_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="pizza_size")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        template = "{0.pizza_type} {0.pizza_style} {0.pizza_size} {0.price}"
        return template.format(self)


class Sub(models.Model):
    desc = models.CharField(max_length=30)

    def __str__(self):
        return self.desc


class Extra(models.Model):
    desc = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.desc


class SubPrice(models.Model):
    sub_type = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="sub_type")
    sub_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="sub_size")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.sub_type} ({self.sub_size}, ${self.price})"


class Pasta(models.Model):
    desc = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.desc} (${self.price})"


class Salad(models.Model):
    desc = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.desc} (${self.price})"


class Platter(models.Model):
    desc = models.CharField(max_length=30)

    def __str__(self):
        return self.desc


class PlatterPrice(models.Model):
    platter_type = models.ForeignKey(Platter, on_delete=models.CASCADE, related_name="platter_type")
    platter_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="platter_size")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.platter_type} ({self.platter_size}, ${self.price})"


class OrderItem(models.Model):
    item = models.CharField(max_length=150)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.item} Qty: {self.quantity} Price: ${self.total}"


class Basket(models.Model):
    items = models.ManyToManyField(OrderItem, through="BasketOrderItem")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_customer")
    start_date = models.DateField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Date: {self.start_date} - Username: {self.customer} - Items: {self.count_items()}" \
            f" - Total: ${self.basket_total()} - Ordered: {self.ordered}"

    def get_id(self):
        return self.id

    def count_items(self):
        return sum([item.quantity for item in self.items.all()])

    def show_basket(self):
        return self.items.all().order_by('item')

    def basket_total(self):
        return sum([item.total for item in self.items.all()])


class BasketOrderItem(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Charge id: {self.stripe_charge_id} - Customer: {self.customer} - Amount: {self.amount}"


class Order(models.Model):
    status = (
        ("Processing your order", "Processing"),
        ("Preparing your order", "Preparing"),
        ("Your order is ready!", "Ready"),
        ("Completed", "Completed")
    )

    order = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="order_basket", blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=status, default='Processing your order')
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=6, decimal_places=2)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):

        order_ref = str(self.id)
        order_ref = order_ref.zfill(6)
        date = self.order_date.strftime('%m/%d/%Y')
        return f"Order Ref: {order_ref} - Date: {date} - Total: ${self.order_total}"
