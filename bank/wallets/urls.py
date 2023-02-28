from django.urls import path
from wallets import views

urlpatterns = [
    path('wallets/', views.snippet_list),
    # path('wallets/<int:pk>/', .),
]