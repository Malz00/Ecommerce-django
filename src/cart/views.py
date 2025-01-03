from django.shortcuts import render, redirect
from product.models import Product
from django.shortcuts import render,redirect
from orders.models import Order
from django.contrib import messages
from .models import Product, Cart
from addresses.forms import AddressForm
from addresses.models import Address
from .models import Cart
from accounts.forms import LoginForm, GuessForm
from billing.models import BillingProfile
from django.http import HttpRequest, JsonResponse

def is_ajax(self):
    return self.headers.get('x-requested-with') == 'XMLHttpRequest'

HttpRequest.is_ajax = is_ajax

def cart_detail_api_view(request):
    cart_obj, new_obj= Cart.objects.new_or_get(request)
    products = [{
                    "id":x.id,
                    "url": x.get_absolute_url(),
                    "name": x.name, 
                    "price": x.price 
                    } 
                  
                    for x in cart_obj.products.all()]
    cart_data = {"products":products, "subtotal": cart_obj.subtotal, "total":cart_obj.total}
    return JsonResponse( cart_data)

def cart_home(request):

    cart_obj, new_obj= Cart.objects.new_or_get(request)
    b = cart_obj.products.all()
    print(b)
    return render (request, "carts/home.html", {"work":cart_obj })


def cart_update(request):
    product_id = request.POST.get('product_id')  # Get product ID from POST data
    
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Sorry, this product is no longer available.")
            return redirect("cart:home")
        
        cart_obj, created = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            messages.success(request, f"{product_obj.name} removed from your cart.")
            product_added = False
        else:
            cart_obj.products.add(product_obj)
            messages.success(request, f"{product_obj.name} added to your cart.")
            product_added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            print("ajax request")
            json_data = {
                "added": product_added,
                "removed": not product_added,
                "cartItemCount": cart_obj.products.count()
            }
            #return JsonResponse({ "message": "error 400"}, status_code=400)
            return JsonResponse(json_data, status=200)

    return redirect("cart:home")


def checkout_home(request):
    # Get or create a cart based on the session
    cart_obj, cart_created = Cart.objects.new_or_get(request) 
    
    # If the cart is empty or newly created, redirect to cart home
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    order_obj = None 
    login_form = LoginForm()
    guest_form = GuessForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()

    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)

        order_obj = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address =Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get( id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()

   
        if request.method == 'POST':
            # Ensure the order is completed
            is_done = order_obj.check_done()
            if is_done:
                order_obj.marked_paid()  # Mark order as paid
                request.session['cart_items'] = 0  # Reset cart item count
                request.session.pop('cart_id', None)  # Safely remove cart_id from session
                return redirect("cart:success")
            
    
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        
    }

    return render(request, 'carts/checkout.html', context)


def checkout_done_view(request):
    context = {}
    return render(request, "carts/checkout_done.html", context)

        