import decimal

from rest_framework import viewsets, status
from rest_framework.response import Response
from wallets.models import Wallet, User, Transaction
from wallets.serializers import WalletSerializer, UserSerializer, UserRegisterSerializer, TransactionSerializer
from rest_framework import mixins, generics, permissions
from wallets.generators import walletname
from django.db.models import Q, Count
from django.http import Http404


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
        wallets = Wallet.objects.filter(owner=self.request.user).count()
        if serializer.is_valid():
            if wallets < 5:
                if serializer.validated_data['currency'] == 'RUB':
                    balance = 100
                else:
                    balance = 3
                serializer.save(owner=self.request.user, name=walletname.namegen(), balance=balance)
        else:
            raise Http404

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

    def perform_create(self, serializer):
        sender = Wallet.objects.get(name=self.kwargs['name'])
        transfer_amount = serializer.validated_data['transfer_amount']
        receiver = serializer.validated_data['receiver']
        st = 'PAID'
        commission = 10

        if serializer.is_valid():

            print(sender.balance,                           # 91.58
                  sender.currency,                          # RUB
                  receiver.currency,                        # USD
                  sender.owner,                             # admin
                  receiver.owner,                           # admin
                  self.kwargs['name'],                      # H85NXULI
                  serializer.validated_data['receiver'])    # 92FNIZMR


            if transfer_amount > sender.balance or sender.currency != receiver.currency:
                st = 'FAILED'
            if sender.owner == receiver.owner:
                commission = 0
                sender.balance -= transfer_amount
                receiver.balance += transfer_amount
            else:
                sender.balance -= transfer_amount * decimal.Decimal(1.1)
                receiver.balance += transfer_amount
            serializer.save(sender=sender,
                            receiver=receiver,
                            transfer_amount=transfer_amount,
                            commission=commission,
                            status=st)


class AllTransactions(generics.ListAPIView):
    '''List of all wallets transactions for current user'''

    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(sender__owner=self.request.user)
        return queryset
