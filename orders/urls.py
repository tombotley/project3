from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete
)

from . import views, utils

urlpatterns = [
    path("", views.index, name="index"),
    path("order", views.create_order, name="order"),
    path("register", views.register, name="register"),
    url(r'login/$', views.login_page, name="login"),  # works with both the /login and /accounts/login paths
    path("logout", views.logout_page, name="logout"),
    path("add-item", views.add_item, name="add_item"),
    path("remove-item/<int:id>/<int:basket_id>", views.remove_item, name="remove_item"),
    path("basket", views.basket, name="basket"),
    path("checkout", views.checkout, name="checkout"),
    path("my-orders", views.orders, name="orders"),
    path("my-orders/history", views.order_history, name="order_history"),
    path("view-order/<int:id>", views.view_order, name="view_order"),
    path("order-admin", views.order_admin, name="order_admin"),
    path("update-status/<int:order_id>/<str:status>", views.update_status, name="update_status"),
    path("basket-count", utils.basket_count, name="basket_count"),
    url(r'^reset-password/$', password_reset, name="reset_password"),
    url(r'^reset-password/done/$', password_reset_done, name="password_reset_done"),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, name="password_reset_confirm"),
    url(r'^reset-password/complete/$', password_reset_complete, name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

