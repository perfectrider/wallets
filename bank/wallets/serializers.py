from rest_framework import serializers
from wallets.models import Customer, Wallet, Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['owner', 'name', 'type', 'currency', 'balance', 'created_on', 'modified_on']
