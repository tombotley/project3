from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Size, Style, Pizza, Topping, PizzaPrice, Sub, Extra, SubPrice, Pasta, Salad, PlatterPrice, OrderItem, Order, Basket
from .forms import Registration, Login

# Create your views here


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

            user = User.objects.create_user\
                (username=form.cleaned_data['username'],
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

        quantity = request.POST['quantity']
        price = PizzaPrice.objects.filter(pizza_type=pizza_id, pizza_style=style_id, pizza_size=size_id).values_list(
            'price', flat=True)
        print(price)
        print(quantity)
        total = price[0] * int(quantity)
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

        item = str(pizza) + ' ' + str(style) + ' Pizza (' + str(size) + ') ' + str(toppings) + ' - '
        print(item)
        order_item, status = OrderItem.objects.get_or_create(item=item, quantity=quantity, total=total)
        print(order_item)
        basket, status = Basket.objects.get_or_create(customer=customer)
        print(basket)
        basket.items.add(order_item)
        basket.save()

    if 'sub_selection' in request.POST:

        sub_id = request.POST['sub_selection']
        sub = Sub.objects.get(pk=sub_id)
        print(sub)

        size_id = request.POST['sub_size_selection']
        size = Size.objects.get(pk=size_id)
        print(size)

        quantity = request.POST['quantity']
        print('qty ' + quantity)

        price = SubPrice.objects.filter(sub_type=sub_id, sub_size=size_id).values_list('price', flat=True)
        print(price)

        extras = ''
        extras_cost = 0

        if request.POST['extra1'] != 'unselected':

            extra_id = request.POST['extra1']
            extra = Extra.objects.get(pk=extra_id)
            extras = extras + str(extra) + ' '
            extras_cost = extras_cost + extra.price
            print(extras)

        if request.POST['extra2'] != 'unselected':

            extra_id = request.POST['extra2']
            extra = Extra.objects.get(pk=extra_id)
            extras = extras + str(extra) + ' '
            extras_cost = extras_cost + extra.price
            print(extras)

        if request.POST['extra3'] != 'unselected':

            extra_id = request.POST['extra3']
            extra = Extra.objects.get(pk=extra_id)
            extras = extras + str(extra) + ' '
            extras_cost = extras_cost + extra.price
            print(extras)

        if request.POST['extra4'] != 'unselected':

            extra_id = request.POST['extra4']
            extra = Extra.objects.get(pk=extra_id)
            extras = extras + str(extra) + ' '
            extras_cost = extras_cost + extra.price
            print(extras)

        print('extra cost ' + str(extras_cost))

    if 'pasta_selection' in request.POST:
        pass

    if 'salad_selection' in request.POST:
        pass

    if 'platter_selection' in request.POST:
        pass

    return redirect('order')


@login_required(login_url='login')
def remove_item(request, id):

    print('Here lies item id, and he is fucking pissed off!')
    print(id)
    item = OrderItem.objects.filter(pk=id)
    item[0].delete()

    return redirect('basket')


@login_required(login_url='login')
def basket(request):

    customer = request.user
    basket = Basket.objects.filter(customer=customer, ordered=False)
    items = basket[0].show_basket()
    count = basket[0].count_items()
    total = basket[0].basket_total()

    context = {
        "items": items,
        "count": count,
        "total": total
    }

    return render(request, 'orders/basket.html', context)
