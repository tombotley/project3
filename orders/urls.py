from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order", views.create_order, name="order"),
    path("register", views.register, name="register"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("add_item", views.add_item, name="add_item"),
    path("remove_item/<int:id>", views.remove_item, name="remove_item"),
    path("basket", views.basket, name="basket")
]
