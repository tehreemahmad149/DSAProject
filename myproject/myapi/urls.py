# myapi/urls.py
from django.urls import path
from .views import SearchView

urlpatterns = [
    path('api/search/', SearchView.as_view(), name='search'),  # Update the URL pattern
    # Add other URL patterns as needed
]
