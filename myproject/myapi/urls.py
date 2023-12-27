# myapi/urls.py
from django.urls import path
from .views import SearchView, AddContentView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search-view'),
    path('add-content/', AddContentView.as_view(), name='add-content-view'),
]