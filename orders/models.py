from django.db import models
from django.contrib.auth.models import User

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
    items = models.ManyToManyField(OrderItem)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_customer")
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Username: {self.customer} - Items: {self.count_items()} - Total: ${self.basket_total()} - Ordered: {self.ordered}"

    def count_items(self):
        return self.items.all().count()

    def show_basket(self):
        return self.items.all()

    def basket_total(self):
        return sum([item.total for item in self.items.all()])


class Order(models.Model):
    status = (
        ("Preparing", "Preparing"),
        ("Ready", "Ready"),
        ("Completed", "Completed")
    )

    order_number = models.CharField(max_length=10)
    order = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="order_basket", blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=status, blank=True)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order No. {self.order_number} - Total: ${Basket.basket_total()} - Date: {self.order_date} - Status: {self.order_status}"
