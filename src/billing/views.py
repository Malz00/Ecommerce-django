from django.shortcuts import render

# Create your views here.
import stripe
from django.http import JsonResponse, HttpRequest, HttpResponse
from is_safe_url import is_safe_url

stripe.api_key='sk_test_51QQSEHL2gtVMUgW2m7gbHKrUKmq7viNxElzS6BBdkPvZrm62InOx4k5XZ1Jz1hkuAxgSEHyBe1GHxFEnlMwvFR4500cjas2fmA'
STRIPE_PUB_KEY = "pk_test_51QQSEHL2gtVMUgW2jv0B7li6posGHMhj66flNPsFxgtUeNhDSHNT6qX5yXfQm22bZCCrvCVDSefAFKHpLgBnsJPm00o6YZZ2qb"

def is_ajax(self):
    return self.headers.get('x-requested-with') == 'XMLHttpRequest'

HttpRequest.is_ajax = is_ajax


def payment_method_view(request):
    next_url = None
    next_ =request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_    

   
    return render(request, 'billing/checkout.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_create_view(request):
    if request.method == 'POST' and request.is_jax():
        print(request.POST)
        return JsonResponse({"message": "success! your card was  addedd"})
    
    return HttpResponse("error", status_code=401)
    # return render(request, 'billing/checkout.html', {"publish_key": STRIPE_PUB_KEY})

    