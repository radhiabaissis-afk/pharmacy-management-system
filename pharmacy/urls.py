from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('sell/<int:pk>/', views.sell_medicine, name='sell_medicine'),
    path('transactions/', views.transaction_list, name='transaction_list'),
]