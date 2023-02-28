from rest_framework import serializers
from wallets.models import Customer, Wallet, Transaction
from django.contrib.auth.models import User

class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Wallet
        fields = ['owner', 'name', 'type', 'currency', 'balance', 'created_on', 'modified_on']

class UserSerializer(serializers.ModelSerializer):
    wallets = serializers.PrimaryKeyRelatedField(many=True, queryset=Wallet.objects.all())
    # in ModelSerializers not included reverse relation, because we added
    # this field here.

    class Meta:
        model = User
        fields = ['id', 'username', 'wallets']