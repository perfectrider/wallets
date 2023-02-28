from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from wallets import views

urlpatterns = [
    path('wallets/', views.WalletsList.as_view()),
    path('wallets/<int:pk>/', views.WalletDetail.as_view()),
    path('customers/', views.CustomerList.as_view()),
    path('customers/<int:pk>/', views.CustomerDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)