from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class   Meta:
        model = Address
        fields = [
            #'billing_profile',
            #'address_type',
            'Address_line_1',
            'Address_line_2',
            'country',
            'city',
            'state',
            'postal_code',
        ]



