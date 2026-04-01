from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('medicines/', views.medicine_list, name='medicine_list'),
    path('add/', views.add_medicine, name='add_medicine'),
    path('sell/<int:pk>/', views.sell_medicine, name='sell_medicine'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add-batch/', views.add_batch, name='add_batch'),

    path('medicine/edit/<int:pk>/', views.edit_medicine, name='edit_medicine'),
    path('medicine/delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
]