from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView, CustomerRegisterView

urlpatterns = [
    path('customer/', CustomerListCreateView.as_view(), name='Customer-list-create'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='Customer-detail'),
    path('customer/register/', CustomerRegisterView.as_view(), name='Customer-register'),
]
