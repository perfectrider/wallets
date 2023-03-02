from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from wallets import views

urlpatterns = [
    # path('wallets/', views.WalletsList.as_view({'get': 'list'})),
    # path('wallets/<int:pk>/', views.WalletsList.as_view({'get': 'retrieve'})),
    # path('walletcreate/', views.WalletCreate.as_view()),
    # path('users/', views.UsersList.as_view()),
    # path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)