from rest_framework import viewsets, status
from rest_framework.response import Response
from wallets.models import Wallet, User, Transaction
from wallets.serializers import WalletSerializer, UserSerializer, UserRegisterSerializer, TransactionSerializer
from rest_framework import mixins, generics, permissions
from wallets.generators import walletname
from django.db.models import Q


class UserRegister(generics.CreateAPIView):
    '''Registration of new user.'''

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class WalletsList(viewsets.ModelViewSet):
    '''List of wallets. List is available only for admin'''

    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'

    def get_queryset(self):
        queryset = Wallet.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        # current user is owner func
        serializer.save(owner=self.request.user, name=walletname.namegen())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersList(generics.ListAPIView):
    '''List of wallets. List is available only for admin'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class TransactionList(viewsets.ModelViewSet):
    '''List of all transactions of current user. Available only for current user.'''

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        walletname = self.kwargs['name']
        if walletname is not None:
            queryset = Transaction.objects.filter(Q(sender__name=walletname) | Q(receiver__name=walletname))
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            Transaction.make_transaction(**serializer.validated_data)
        except ValueError:
            # content = {'error': 'Not enough money on the current wallet!'}
            return Response(status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

class AllTransactions(generics.ListAPIView):
    '''List of all wallets transactions for current user'''

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(sender__owner=self.request.user)
        return queryset