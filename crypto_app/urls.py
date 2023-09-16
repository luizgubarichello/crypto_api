from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.GenerateAddressView.as_view(), name='generate'),
    path('list/', views.ListAddressView.as_view(), name='list'),
    path('retrieve/<int:pk>/', views.RetrieveAddressView.as_view(), name='retrieve'),
]
