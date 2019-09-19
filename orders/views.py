from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from .models import Size, Style, Pizza, Topping, PizzaPrice, Sub, Extra, SubPrice, Pasta, Salad, PlatterPrice,\
    OrderItem, Order, Payment, Basket, BasketOrderItem
from .forms import Registration, Login

import stripe

stripe.api_key = ""


def index(request):

    return render(request, 'orders/index.html')


def register(request):

    # if form data posted, process data
    if request.method == 'POST':

        # bind POST data to instance of Registration form
        form = Registration(request.POST)

        # check username and email aren't already in use and passwords match (try/except)

        # if data is valid, register the user
        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'])

            user.save()

            return redirect('login')

    # else if GET request, create registration form to render with register.html
    else:
        form = Registration()

    return render(request, 'orders/accounts/register.html', {'form': form})


def login_page(request):

    # if form data posted, process data
    if request.method == 'POST':

        # bind POST data to instance of Login form
        form = Login(request.POST)

        # if data is valid, check user credentials
        if form.is_valid():

            # check username and password are correct
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:

                login(request, user)
                return redirect('index')

            else:

                return render(request, 'orders/accounts/login.html', {
                    'form': form, 'error': 'Username or password incorrect'})


    # else if GET request, create Login form to render with login.html
    else:
        form = Login()

    return render(request, 'orders/accounts/login.html', {'form': form})


@login_required(login_url='index')
def logout_page(request):

    logout(request)

    return render(request, 'orders/accounts/logout.html')


@login_required(login_url='login')
def create_order(request):

    context = {
        "sizes": Size.objects.all(),
        "styles": Style.objects.all(),
        "toppings": Topping.objects.all(),
        "pizzas": Pizza.objects.all(),
        "pizza_prices": PizzaPrice.objects.all(),
        "subs": Sub.objects.all(),
        "extras": Extra.objects.all(),
        "sub_prices": SubPrice.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platter_prices": PlatterPrice.objects.all()
    }

    return render(request, 'orders/order.html', context)


@login_required(login_url='login')
def add_item(request):

    customer = request.user

    if 'pizza_selection' in request.POST:

        pizza_id = request.POST['pizza_selection']
        pizza = Pizza.objects.get(pk=pizza_id)

        style_id = request.POST['style_selection']
        style = Style.objects.get(pk=style_id)

        size_id = request.POST['pizza_size_selection']
        size = Size.objects.get(pk=size_id)

        quantity = int(request.POST['quantity'])
        price = PizzaPrice.objects.filter(pizza_type=pizza_id, pizza_style=style_id, pizza_size=size_id).values_list(
            'price', flat=True)
        total = price[0] * quantity
        toppings = ''

        if request.POST['topping1'] != 'unselected':

            topping_id = request.POST['topping1']
            topping = Topping.objects.get(pk=topping_id)
            toppings = ' - w/ ' + str(topping)

            if request.POST['topping2'] != 'unselected':

                topping_id = request.POST['topping2']
                topping = Topping.objects.get(pk=topping_id)
                toppings = toppings + ', ' + str(topping)

                if request.POST['topping3'] != 'unselected':

                    topping_id = request.POST['topping3']
                    topping = Topping.objects.get(pk=topping_id)
                    toppings = toppings + ', ' + str(topping)

        item = str(style) + ' ' + str(pizza) + ' Pizza (' + str(size) + ') ' + str(toppings) + ' - '
        order_item, status = OrderItem.objects.get_or_create(item=item, quantity=quantity, total=total)
        basket, status = Basket.objects.get_or_create(customer=customer, ordered=False)
        BasketOrderItem.objects.create(order_item=order_item, basket=basket)
        basket.save()

    if 'sub_selection' in request.POST:

        sub_id = request.POST['sub_selection']
        sub = Sub.objects.get(pk=sub_id)

        size_id = request.POST['sub_size_selection']
        size = Size.objects.get(pk=size_id)

        quantity = int(request.POST['quantity'])

        price = SubPrice.objects.filter(sub_type=sub_id, sub_size=size_id).values_list('price', flat=True)
        total = price[0] * quantity

        extras = ''
        extras_cost = 0

        if request.POST['extra1'] != 'unselected':

            extra_id = request.POST['extra1']
            extra = Extra.objects.get(pk=extra_id)
            extras = extras + str(extra) + ', '
            extras_cost = extras_cost + extra.price

        if request.POST['extra2'] != 'unselected':

            extra_id = request.POST['extra2']
            extra = Extra.objects.get(pk=extra_id)
            extras = extras + str(extra) + ', '
            extras_cost = extras_cost + extra.price

        if request.POST['extra3'] != 'unselected':

            extra_id = request.POST['extra3']
            extra = Extra.objects.get(pk=extra_id)
            extras = extras + str(extra) + ', '
            extras_cost = extras_cost + extra.price

        if request.POST['extra4'] != 'unselected':

            extra_id = request.POST['extra4']
            extra = Extra.objects.get(pk=extra_id)
            extras = extras + str(extra)
            extras_cost = extras_cost + extra.price

        if len(extras) > 0:
            extras = ' - w/ Extra ' + extras
            if extras.endswith(', '):
                extras = extras[:-2]
            total = extras_cost * quantity + total

        item = str(sub) + ' Sub (' + str(size) + ') ' + str(extras) + ' - '
        order_item, status = OrderItem.objects.get_or_create(item=item, quantity=quantity, total=total)
        basket, status = Basket.objects.get_or_create(customer=customer, ordered=False)
        BasketOrderItem.objects.create(order_item=order_item, basket=basket)
        basket.save()

    if 'pasta_selection' in request.POST:

        pasta_id = request.POST['pasta_selection']
        pasta = Pasta.objects.get(pk=pasta_id)

        quantity = int(request.POST['quantity'])

        price = Pasta.objects.filter(pk=pasta_id).values_list('price', flat=True)
        total = price[0] * quantity

        item = str(pasta.desc) + ' - '
        order_item, status = OrderItem.objects.get_or_create(item=item, quantity=quantity, total=total)
        basket, status = Basket.objects.get_or_create(customer=customer, ordered=False)
        BasketOrderItem.objects.create(order_item=order_item, basket=basket)
        basket.save()

    if 'salad_selection' in request.POST:

        salad_id = request.POST['salad_selection']
        salad = Salad.objects.get(pk=salad_id)

        quantity = int(request.POST['quantity'])

        price = Salad.objects.filter(pk=salad_id).values_list('price', flat=True)
        total = price[0] * quantity

        item = str(salad.desc) + ' - '
        order_item, status = OrderItem.objects.get_or_create(item=item, quantity=quantity, total=total)
        basket, status = Basket.objects.get_or_create(customer=customer, ordered=False)
        BasketOrderItem.objects.create(order_item=order_item, basket=basket)
        basket.save()

    if 'platter_selection' in request.POST:

        platter_id = request.POST['platter_selection']
        platter = PlatterPrice.objects.get(pk=platter_id)

        quantity = int(request.POST['quantity'])

        price = PlatterPrice.objects.filter(pk=platter_id).values_list('price', flat=True)
        total = price[0] * quantity

        item = str(platter.platter_type) + ' Platter (' + str(platter.platter_size) + ') - '
        order_item, status = OrderItem.objects.get_or_create(item=item, quantity=quantity, total=total)
        basket, status = Basket.objects.get_or_create(customer=customer, ordered=False)
        BasketOrderItem.objects.create(order_item=order_item, basket=basket)
        basket.save()

    messages.success(request, 'Item added')
    return redirect('order')


@login_required(login_url='login')
def remove_item(request, id, basket_id):

    item = BasketOrderItem.objects.filter(order_item=id, basket=basket_id)
    item[0].delete()

    customer = request.user
    basket = Basket.objects.filter(customer=customer, ordered=False)

    if basket[0].count_items() == 0:
        Basket.objects.filter(id=basket_id).delete()

    return redirect('basket')


@login_required(login_url='login')
def basket(request):

    customer = request.user
    basket = Basket.objects.filter(customer=customer, ordered=False)
    context = {}

    if basket:
        items = basket[0].show_basket()
        count = basket[0].count_items()
        total = basket[0].basket_total()
        basket_id = basket[0].get_id()

        context = {
            "items": items,
            "count": count,
            "total": total,
            "basket_id": basket_id
        }

    return render(request, 'orders/basket.html', context)


@login_required(login_url='login')
def checkout(request):

    customer = request.user
    basket = Basket.objects.get(customer=customer, ordered=False)

    if not basket:
        raise Http404('Basket not found.')

    if request.method == 'POST':

        total = int(basket.basket_total() * 100)
        token = request.POST.get('stripeToken')

        if token is None:
            raise Http404('Payment not found.')

        try:
            # Use Stripe's library to make requests...
            charge = stripe.Charge.create(
                amount=int(total),
                currency="usd",
                source="tok_visa",
            )

            payment = Payment()
            payment.stripe_charge_id = charge.id
            payment.customer = customer
            payment.amount = total
            payment.save()

            order = Order()
            order.order = basket
            order.order_total = basket.basket_total()
            order.payment = payment
            order.save()

            basket.ordered = True
            basket.save()

            customer_name = request.user.first_name
            customer_email = request.user.email

            send_mail("Order Confirmation - Pinocchio's Pizza",
                      f"Dear {customer_name},\n\n"
                      f"We have received your payment and will shortly begin preparing your order!\n"
                      f"You will receive an email when your order is ready for collection. You can also check the "
                      f"status in the 'Your Orders' page of our website.\n\n"
                      f"Thank you for choosing Pinocchio's Pizza & Subs!\n\n"
                      f"{order}",
                      "webmaster@localhost",
                      [customer_email],
                      fail_silently=False)

            messages.success(request, 'Thanks! Payment complete! We have received your order.')
            return redirect('orders')

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"{err.get('message')}")
            return redirect(reverse('checkout'))

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "Rate limit error")
            return redirect(reverse('checkout'))

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid request")
            return redirect(reverse('checkout'))

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Authentication error")
            return redirect(reverse('checkout'))

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "Connection error")
            return redirect(reverse('checkout'))

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(request, "An error occurred, payment cancelled. Please try again!")
            return redirect(reverse('checkout'))

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(request, "An error occurred, payment cancelled.")
            return redirect(reverse('checkout'))

    else:

        context = {}

        if basket:
            total = basket.basket_total()

            context = {
                "total": total,
            }

        return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
def orders(request):

    customer = request.user
    orders = Order.objects.filter(order__customer=customer).exclude(order_status='Completed').order_by('-order_date')
    context = {}

    if orders:

        context = {
            "orders": orders
        }

    return render(request, 'orders/orders.html', context)


@login_required(login_url='login')
def order_history(request):

    customer = request.user
    orders = Order.objects.filter(order__customer=customer, order_status='Completed').order_by('-order_date')
    context = {}

    if orders:

        context = {
            "orders": orders
        }

    return render(request, 'orders/order_history.html', context)


@login_required(login_url='login')
def view_order(request, id):

    order = Order.objects.filter(id=id)
    basket = Basket.objects.filter(order_basket__id=id)
    items = basket[0].show_basket()

    context = {
        "items": items,
        "order": order
    }

    return render(request, 'orders/view_order.html', context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def order_admin(request):

    orders = Order.objects.all().exclude(order_status='Completed').order_by('-order_date')
    context = {}

    if orders:

        context = {
            "orders": orders
        }

    return render(request, 'orders/order_admin.html', context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def update_status(request, order_id, status):

    print(order_id)
    print(status)

