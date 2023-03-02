from rest_framework import serializers
from wallets.models import Wallet
from django.contrib.auth.models import User

class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.ReadOnlyField()

    class Meta:
        model = Wallet
        fields = ['id', 'owner', 'name', 'type', 'currency', 'balance', 'created_on', 'modified_on']

class UserSerializer(serializers.ModelSerializer):
    wallets = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'wallets']