from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView,DetailView

from cart.models import Cart
from .models import Product
from django.http import Http404

from analytics.mixing import ObjectViewedMixing



class ProductFeaturedListView(ListView):
    
    template_name = "products/list.html"
   

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(ObjectViewedMixing, DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured_detail.html"




#     def get_contect_data(self, *args, **kwargs):
#         context =super(ProductDetailSlugView, self).get_context_data( *args,**kwargs)
#         cart_obj = Cart.objects.new_or_get(self.request)
#         context['cart'] = cart_obj
#         return context



class ProductDetailSlugView(ObjectViewedMixing, DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        # Get the context from the parent class
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        
        # Get the request object
        request = self.request
        
        # Get or create a cart (handles both authenticated and anonymous users)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        
        # Add the cart to the context to use in the template
        context['cart'] = cart_obj

        return context

    def get_object(self, *args, **kwargs): 
        # Get the slug from the URL
        slug = self.kwargs.get('slug')
        
        
        try:
            # Try to retrieve the product
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            # If the product is not found, raise a 404
            raise Http404("Not found")
        except Product.MultipleObjectsReturned:
            # If there are multiple products with the same slug, take the first one
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except Exception as e:
            # Catch any other errors and raise a generic exception (optional)
            raise Http404("An unexpected error occurred")

        #object_viewed_signal.send(instance.__class__, instance=instance, request=self.request)
        return instance
 
 




class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        request = self.request
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context
  
    def get_queryset(self, *args, **kwargs):
        request = self.request

        return Product.objects.all() 



def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }

    return render (request, "products/list.html", context)



class ProductDetailView(ObjectViewedMixing, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs ):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context
    
    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404('products doesnt exist')

        return instance


def product_detail_view(request, pk= None,*args, **kwargs ):
    #instance = Product.objects.get(pk=pk)
    #instance = get_object_or_404(Product, pk=pk)
    # try:
       
    #    instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print("No product here")
    #     raise Http404('products doesnt exist')
    # except:
    #     print("huuh")


    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404('products doesnt exist')

    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404('products doesnt exist')


    context = {
        'object': instance
    }

    return render (request, "products/detail.html", context)


