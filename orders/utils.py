from django.http import JsonResponse
from .models import Basket


def basket_count(request):

    customer = request.user
    basket = Basket.objects.filter(customer=customer, ordered=False)
    context = {}

    if basket:
        count = basket[0].count_items()

        context = {
            "count": count,
        }

    else:
        pass

    return JsonResponse(context)
