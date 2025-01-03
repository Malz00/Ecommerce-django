from django.shortcuts import redirect
from .forms import AddressForm
from is_safe_url import is_safe_url
from billing.models import BillingProfile

from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from .forms import AddressForm
from .models import BillingProfile, Address


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {"form": form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        print("Form is valid!")
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, created = BillingProfile.objects.new_or_get(request)  # Retrieve or create billing profile
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile  # Assign billing profile to address
            instance.address_type = request.POST.get('address_type', 'shipping')  # Set address type
            instance.save()  # Save the address instance

            request.session[address_type + "_address_id" ]= instance.id
            print( address_type + "_address_id" )
    

        else:
            return redirect("cart:checkout")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("cart:checkout")

    print("Form is invalid!", form.errors)
    return redirect("cart:checkout")



def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        context = {}
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method =="POST":
            print(request.method)
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, created = BillingProfile.objects.new_or_get(request)  # Retrieve or create billing profile
            if shipping_address is not None:

                qs= Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id" ]= shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("cart:checkout")
