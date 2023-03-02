from rest_framework import viewsets
from wallets.models import Wallet, User
from wallets.serializers import WalletSerializer, UserSerializer, UserRegisterSerializer
from rest_framework import mixins, generics, permissions
from wallets.generators import walletname


class UserRegister(generics.CreateAPIView):
    '''Registration of new user.'''

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class WalletsList(viewsets.ModelViewSet, mixins.CreateModelMixin):
    '''List of wallets. List is available only for admin'''

    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'

    def get_queryset(self):
        queryset = Wallet.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        # current user is owner func
        serializer.save(owner=self.request.user, name=walletname.name_gen())


class UsersList(generics.ListAPIView):
    '''List of wallets. List is available only for admin'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
