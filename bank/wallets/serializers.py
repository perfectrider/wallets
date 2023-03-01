from rest_framework import serializers
from wallets.models import Wallet
from django.contrib.auth.models import User

class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.ReadOnlyField()

    class Meta:
        model = Wallet
        fields = ['id', 'owner', 'name', 'type', 'currency', 'balance', 'created_on', 'modified_on']

class WalletNameSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()

    class Meta:
        model = Wallet
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    # wallets = serializers.PrimaryKeyRelatedField(many=True, queryset=Wallet.objects.all())
    wallets = WalletNameSerializer(many=True)
    # in ModelSerializers not included reverse relation, because we added
    # this field here.

    class Meta:
        model = User
        fields = ['id', 'username', 'wallets']