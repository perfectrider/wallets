from django.contrib.auth.models import User
from rest_framework import status, viewsets, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wallets.models import Wallet, User
from wallets.serializers import WalletSerializer, UserSerializer, UserRegistrSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics, permissions
from wallets.permissions import IsAdminOrOwner
from wallets.generators import walletname


# class WalletsList(generics.ListCreateAPIView):
#     '''All wallets view'''
#
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer
#     permission_classes = [permissions.IsAdminUser]
#
#     def perform_create(self, serializer):
#         # current user is owner func
#         serializer.save(owner=self.request.user, name=walletname.NameGen())
#
# class WalletDetail(generics.RetrieveUpdateDestroyAPIView):
#     '''Detail wallet view'''
#
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer
#     permission_classes = [IsAdminOrOwner]


# class UserList(generics.ListAPIView):
#     '''All users view'''
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAdminUser]

# --------------------------------------------

class UserRegistr(generics.CreateAPIView):
    '''Regisrtation of new user.'''

    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [permissions.AllowAny]


class WalletsList(viewsets.ModelViewSet, mixins.CreateModelMixin):
    '''List of wallets. List is avaliable only for admin'''

    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Wallet.objects.filter(owner=self.request.user)
        return queryset

    def get_object(self):
        return Wallet.objects.get(name=self.name)

    def perform_create(self, serializer):
        # current user is owner func
        serializer.save(owner=self.request.user, name=walletname.NameGen())


class UsersList(generics.ListAPIView):
    '''List of wallets. List is avaliable only for admin'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

