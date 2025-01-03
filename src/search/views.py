from django.views.generic import ListView
from product.models import Product
from django.views.generic.list import ListView



class SearchProductListView(ListView):   
    template_name = "search/view.html"
    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        print(query)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()

# class SearchProductListView(ListView):
#     template_name = "search/view.html"
#     context_object_name = "object_list"
#     paginate_by = 10  # Optional: Add pagination for results

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['query'] = self.request.GET.get('q')
#         return context

#     def get_queryset(self, *args, **kwargs):
#         query = self.request.GET.get('q', None)
#         qs = Product.objects.search(query) if query else Product.objects.featured()
        
#         if self.request.is_ajax():  # AJAX request handling
#             results_html = render_to_string("search/_results.html", {"object_list": qs})
#             return JsonResponse({"html": results_html})
        
#         return qs

