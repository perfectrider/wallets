from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wallets.models import Wallet
from wallets.serializers import WalletSerializer

@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Wallet.objects.all()
        serializer = WalletSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)