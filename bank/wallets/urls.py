from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from wallets import views

urlpatterns = [
    path('registration/', views.UserRegister.as_view()),
    path('users/', views.UsersList.as_view()),
    path('wallets/', views.WalletsList.as_view({'get': 'list', 'put': 'create'})),
    path('wallets/<name>/', views.WalletsList.as_view({'get': 'retrieve'})),
    path('wallets/<name>/transactions', views.TransactionList.as_view({'get': 'list', 'put': 'create'})),
    path('wallets/<name>/transactions/<pk>', views.TransactionList.as_view({'get': 'retrieve'}))
]

urlpatterns = format_suffix_patterns(urlpatterns)
