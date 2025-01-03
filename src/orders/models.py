from django.db import models
from cart.models import Cart
import math
from addresses.models import Address
from billing.models import BillingProfile
from django.db.models.signals import pre_save, m2m_changed, post_save
from ecommerce.utils import unique_order_id_generator

ORDER_STATUS_CHOICE = (
    ('created', 'Created' ),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)
class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        
        if qs.count() == 1:
            
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj

class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.SET_NULL  )
    order_id        = models.CharField(max_length=12, blank=True)
    
    shipping_address = models.ForeignKey(Address, null=True, related_name="shipping_address", blank=True, on_delete=models.SET_NULL  )
    billing_address =   models.ForeignKey(Address, null=True, related_name="billing_address", blank=True, on_delete=models.SET_NULL  )

    cart            = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    status          = models.CharField(max_length=53, default='created', choices=ORDER_STATUS_CHOICE)
    shipping_total  =  models.DecimalField(default=5.99, max_digits= 67, decimal_places=2)
    total           = models.DecimalField(default=0.00, max_digits=67, decimal_places=2)
    active          = models.BooleanField(default=True)
    


    objects = OrderManager()
    def __str__(self):
        return self.order_id
    
    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([ cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return  formatted_total
    
    def check_done(self):
        """Check if the order has all the required fields completed."""
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total

        # Ensure all required fields are present and total is greater than zero
        if billing_profile and shipping_address and billing_address and (total > 0):
            return True
        return False

    def marked_paid(self):
        """Mark the order as paid if all conditions are met."""
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status

def pre_save_created_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_created_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("updating first")
        instance.update_total()

post_save.connect(post_save_order, sender=Order)