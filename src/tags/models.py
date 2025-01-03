from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from ecommerce.utils import unique_slug_generator
from product.models import Product



class Tag(models.Model):
    title       =models.CharField(max_length=225)
    slug        = models.SlugField()
    timestamp   = models.DateField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title

def tag_pre_save_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_reciver, sender=Tag)
