from rest_framework import serializers
from wallets.models import Customer, Wallet, Transaction
from django.contrib.auth.models import User

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['owner', 'name', 'type', 'currency', 'balance', 'created_on', 'modified_on']

class CustomerSerializer(serializers.ModelSerializer):
    wallets = serializers.PrimaryKeyRelatedField(many=True, queryset=Wallet.objects.all())
    # in ModelSerializers not included reverse relation, because we added
    # this field here.

    class Meta:
        model = Customer
        fields = ['id', 'name', 'wallets', 'created_on']