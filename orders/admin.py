from django.contrib import admin
from .models import Pizza, Topping, Style, Size, PizzaPrice, Sub, Extra, SubPrice, Pasta, Salad, Platter, PlatterPrice, Order, OrderItem, Basket

# Register your models here.

admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Style)
admin.site.register(Size)
admin.site.register(PizzaPrice)
admin.site.register(Sub)
admin.site.register(Extra)
admin.site.register(SubPrice)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Platter)
admin.site.register(PlatterPrice)
admin.site.register(Order)
admin.site.register(Basket)
admin.site.register(OrderItem)
