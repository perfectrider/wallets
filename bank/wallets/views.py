from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wallets.models import Wallet
from wallets.serializers import WalletSerializer
from rest_framework.views import APIView
from django.http import Http404

# class WalletsViewSet(viewsets.ModelViewSet):
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer

class WalletsList(APIView):
    '''List of all wallets. Create new wallet'''

    def get(self, request, format=None):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WalletDetail(APIView):
    '''Retrieve, update or delete wallet'''

    def get_object(self, pk):
        try:
            return Wallet.objects.get(pk=pk)
        except Wallet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        wallet = self.get_object(pk)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        wallet = self.get_object(pk)
        serializer = WalletSerializer(wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        wallet = self.get_object(pk)
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)