from django.db import models
from django.conf import settings
from decimal import Decimal
from product.models import Product
from django.db.models.signals import pre_save,post_save, m2m_changed
from django.db import models


User= settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        session_key = request.session.get('cart_id', None)

        if user.is_authenticated:
            # Ensure only one cart exists per user
            cart_qs = self.get_queryset().filter(user=user)
        else:
            # Ensure only one cart exists per session key
            cart_qs = self.get_queryset().filter(session_key=session_key)

        if cart_qs.exists():
            cart = cart_qs.first()
            # Handle duplicates by deleting extras
            cart_qs.exclude(id=cart.id).delete()
            return cart, False
        else:
            # Create a new cart
            cart = self.model.objects.create(
                user=user if user.is_authenticated else None,
                session_key=session_key if not user.is_authenticated else None
            )
            request.session['cart_id'] = cart.id  # Store cart ID in session
            return cart, True

    

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

 
class Cart(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=120, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal     =  models.DecimalField( default=0.00, max_digits=24, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    objects = CartManager()  # This line links the CartManager to the model

    def __str__(self):
        return str(self.id)
    
    
    def __str__(self):
        return f"Cart for {self.user}" if self.user else "Anonymous Cart"
    
   
   
 
    
def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action =='post_remove' or action =='post_clear':
        result = instance.products.all()
        total = 0
        for x in result:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()
        
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_reciever(sender, instance, *args, **kwargs):
    if instance.subtotal > 0: 
        instance.total = Decimal(instance.subtotal) + Decimal(1.08)
    else: 
        instance.total = 0.00
pre_save.connect(pre_save_cart_reciever, sender=Cart)
