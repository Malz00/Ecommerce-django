from django.urls import path


from search.views import (
    SearchProductListView
    
)

urlpatterns = [
    path('',SearchProductListView.as_view(), name='query')

]

