from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from accounts.models import GuestEmail, User

import stripe

stripe.api_key='sk_test_51QQSEHL2gtVMUgW2m7gbHKrUKmq7viNxElzS6BBdkPvZrm62InOx4k5XZ1Jz1hkuAxgSEHyBe1GHxFEnlMwvFR4500cjas2fmA'



User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')  # Corrected session key
        created = False
        obj = None
        
        if user.is_authenticated:
            # For logged-in user checkout
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)

        

        elif guest_email_id is not None:
            # For guest user checkout
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            
            # Serialize the GuestEmail object into a dictionary
            data = {
                'email': guest_email_obj.email,
                'active': guest_email_obj.active,
                'timestamp': guest_email_obj.timestamp.isoformat() if guest_email_obj.timestamp else None,  # Ensure datetime is converted to a string
            }
            
            # Store the serialized data in session
            request.session['guest_email'] = data  # Now this is JSON serializable
            
            # Create or get the BillingProfile object
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)

        else:
            pass

        return obj, created



class BillingProfile(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, null=True, blank=True )
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateField(auto_now=True)
    timestamp   = models.DateField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    objects= BillingProfileManager()

    def __str__(self):
        return self.email



def billing_profile_created_reciver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("send to stripe/braintree")
        customer = stripe.Customer.create(
            email= instance.email
        )
        print(customer)
        instance.customer_id = customer.id

pre_save.connect( billing_profile_created_reciver, sender=BillingProfile)

def user_created_reciever(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_reciever, sender=User)

