from django.db import models
import random
import os
from ecommerce.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
# Create your models here.
from django.urls import reverse
from django.db.models import Q


def get_filename_exist (filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)

    return name, ext 

def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1, 31868869)
    name, ext = get_filename_exist(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
        )

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter( active=True )
    
    def featured(self):
        return self.filter(featured=True, active=True)
    
    def search(self, query):


        lookups = (Q(title__icontains=query)|
                   Q(price__icontains=query)|
                    Q(description__icontains=query)|
                    Q(tag__title__icontains=query)
                    
                    ) 
        
        return self.filter(lookups).distinct()
    
class ProductManger(models.Manager):
    def all(self):
        return self.get_queryset().active()

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    def featured(self):
        return self.get_queryset().filter(featured=True) 

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    
    def search(self, query):
        return self.get_queryset().active().search(query)
    
    

class Product(models.Model):
    title                 = models.CharField(max_length=56)
    slug                  = models.SlugField(default="abc", blank=True, unique=True)
    description           = models.TextField()
    price                 = models.DecimalField(decimal_places=2, max_digits=12, default=12.99)
    image                 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured              = models.BooleanField(default=False)
    active                = models.BooleanField(default=True)
    timestamp              = models.DateField(auto_now_add=True)
    objects = ProductManger()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

   
    def __str__(self):
        return self.title
    
    @property
    def name(self):
        return self.title

    
def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_reciever, sender=Product)

